# Disk Clear Utility (Windows) — NIST 800-88 Standard

## Quick Pitch to Jury
> *“This program opens a physical drive, locks the filesystem if present, writes zeros to every logical block the host can reach, flushes the device cache, and optionally reads back the data to verify that every byte is zero — a standard ‘Clear’ per NIST 800-88, audited by readback verification.”*

---

## Header & Macros — Environment Setup

```c
#define _CRT_SECURE_NO_WARNINGS
#include <windows.h>
#include <winioctl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
```

**Purpose:** Include Windows APIs and C runtime functions we need (file I/O, device controls, memory, strings).  
**What to say:** “We use standard Windows system APIs to talk safely to the operating system and the drive.”

---

### Compatibility Helpers

```c
#ifndef CTL_CODE
#define CTL_CODE(...) ...
#endif
#ifndef FILE_DEVICE_FILE_SYSTEM
#define FILE_DEVICE_FILE_SYSTEM 0x00000009
#endif
#ifndef METHOD_BUFFERED
#define METHOD_BUFFERED 0
#endif
#ifndef FILE_ANY_ACCESS
#define FILE_ANY_ACCESS 0
#endif
```

**Purpose:** Define control-code helpers (for MinGW compatibility).  
**What to say:** “Compatibility glue so the program compiles across common Windows C toolchains.”

---

### Volume Control Codes

```c
#ifndef FSCTL_LOCK_VOLUME
#define FSCTL_LOCK_VOLUME    CTL_CODE(FILE_DEVICE_FILE_SYSTEM, 6, METHOD_BUFFERED, FILE_ANY_ACCESS)
#define FSCTL_UNLOCK_VOLUME  CTL_CODE(FILE_DEVICE_FILE_SYSTEM, 7, METHOD_BUFFERED, FILE_ANY_ACCESS)
#define FSCTL_DISMOUNT_VOLUME CTL_CODE(FILE_DEVICE_FILE_SYSTEM, 8, METHOD_BUFFERED, FILE_ANY_ACCESS)
#endif
```

**Purpose:** Define the device control codes we use to lock, dismount and unlock a volume.  
**What to say:** “These are the exact system calls we’ll ask Windows to perform to safely take the filesystem offline.”

---

### Buffer Size

```c
#define BUF_SIZE (16ULL * 1024 * 1024)
```

**Purpose:** Use a 16 MiB buffer for read/write operations.  
**What to say:** “Writes occur in 16-megabyte chunks for reasonable speed without hogging RAM.”

---

## Usage & Helper Functions

### Usage Function

```c
static void usage(const char *prog) { ... }
```

**Purpose:** Prints how to run the program.  
**What to say:** “This message tells an operator how to run the tool and explains test/verify options.”

---

### Disk Length Function

```c
static int get_disk_length(HANDLE hDrive, unsigned long long *out_len) { ... }
```

**Purpose:** Uses `DeviceIoControl(..., IOCTL_DISK_GET_LENGTH_INFO)` to query logical disk size.  
**What to say:** “We ask the OS for the exact logical length of the device and then plan writes to cover that exact range.”

---

## Main — Argument Parsing

```c
if (argc < 3) { usage(argv[0]); return 1; }
const char *driveNumStr = argv[1];
const char *volArg = argv[2];
int testMode = 0, verifyMode = 0;
for (int i = 3; i < argc; i++) { ... }
```

**Purpose:** Parse physical drive number, volume letter (or `NONE`), plus options `--test` and `--verify`.  
**What to say:** “The operator specifies which physical drive to wipe and whether to do a dry-run or a read-back verification.”

---

## Device Path

```c
snprintf(physicalPath, sizeof(physicalPath), "\\\\.\\PhysicalDrive%s", driveNumStr);
```

**Purpose:** Build raw device path (e.g., `\\.\PhysicalDrive1`).  
**What to say:** “We open the physical device directly rather than a filesystem file.”

---

## Safety Confirmation

```c
printf("Type the word 'CONFIRM' ...");
if (!fgets(confirm, sizeof(confirm), stdin)) return 1;
confirm[strcspn(confirm, "\r\n")] = 0;
if (strcmp(confirm, "CONFIRM") != 0) { printf("Aborted..."); return 1; }
```

**Purpose:** Prevents accidental runs.  
**What to say:** “Operator must type CONFIRM — this is an explicit, documented safety step.”

---

## Lock & Dismount Volume

```c
if (strcmp(volArg, "NONE") != 0) {
    snprintf(volPath, sizeof(volPath), "\\\\.\\%s:", volArg);
    hVolume = CreateFileA(...);
    DeviceIoControl(hVolume, FSCTL_LOCK_VOLUME, ...);
    DeviceIoControl(hVolume, FSCTL_DISMOUNT_VOLUME, ...);
    printf("Volume %s: locked and dismounted successfully.\n", volArg);
}
```

**Purpose:** Ensure exclusive access to device.  
**What to say:** “We politely ask the OS to lock and dismount the file system so we have exclusive, consistent access. If we can’t get exclusive access, the tool aborts.”

---

## Open the Physical Drive

```c
HANDLE hDrive = CreateFileA(physicalPath, GENERIC_READ | GENERIC_WRITE,
    FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING,
    FILE_FLAG_WRITE_THROUGH, NULL);
```

**Purpose:** Open drive with write-through semantics.  
**What to say:** “We open the drive for raw read/write and request that writes be sent through to the device for integrity.”

---

## Query Disk Length

```c
unsigned long long disk_len = 0;
if (!get_disk_length(hDrive, &disk_len)) { ... }
else printf("Disk length reported: %llu bytes (~%llu MB)\n", disk_len, disk_len/(1024ULL*1024ULL));
```

**Purpose:** Prefer exact length from OS.  
**What to say:** “When available, we write the exact logical size the OS gives us — this avoids overshooting or guessing.”

---

## Allocate & Zero Buffer

```c
void *buf = VirtualAlloc(NULL, BUF_SIZE, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
memset(buf, 0, BUF_SIZE);
```

**Purpose:** Allocate 16 MiB buffer of zeros.  
**What to say:** “We prepare a 16MB chunk of zeros and repeatedly write that to the device.”

---

## Overwrite Logic

### Test Mode
```c
if (testMode) {
    SetFilePointerEx(hDrive, offset0, NULL, FILE_BEGIN);
    WriteFile(hDrive, buf, (DWORD)BUF_SIZE, &written, NULL);
    FlushFileBuffers(hDrive);
}
```

**Purpose:** Validate path and permissions.  
**What to say:** “Test mode writes one 16MB block to validate the write path without wiping the whole drive.”

---

### Full Mode
```c
if (disk_len > 0) {
    while (remaining > 0) { ...progress... }
} else {
    while (1) { ...fallback... }
}
FlushFileBuffers(hDrive);
```

**Purpose:** Write zeros across entire disk capacity.  
**What to say:** “We write zeros across the entire reported logical capacity, reporting progress and flushing caches at the end to ensure persistence.”

---

## Verification (Optional)

```c
if (verifyMode) {
    SetFilePointerEx(hDrive, off0, NULL, FILE_BEGIN);
    while (ReadFile(hDrive, buf, BUF_SIZE, &readBytes, NULL)) {
        for (...) if (b[i] != 0x00) { ...fail... }
    }
}
```

**Purpose:** Read back and confirm all bytes are zero.  
**What to say:** “The verification pass checks every byte. Non-zero bytes mean hidden sectors, remapped blocks, or device errors.”

---

## Cleanup

```c
VirtualFree(buf, 0, MEM_RELEASE);
CloseHandle(hDrive);
if (hVolume != INVALID_HANDLE_VALUE) {
    DeviceIoControl(hVolume, FSCTL_UNLOCK_VOLUME, ...);
    CloseHandle(hVolume);
}
printf("Clear operation finished.\n");
```

**Purpose:** Free memory, close handles, unlock volume.  
**What to say:** “We clean up all handles and resources and report a final audit message summarizing the operation.”

---
