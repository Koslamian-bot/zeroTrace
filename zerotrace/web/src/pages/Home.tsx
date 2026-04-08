import React from 'react';
import { motion } from 'framer-motion';
import { 
  Shield, 
  Lock, 
  CheckCircle2, 
  Download, 
  ArrowRight, 
  Cpu, 
  FileText, 
  Zap, 
  Server,
  CloudLightning,
  EyeOff
} from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, description, delay }: { icon: any, title: string, description: string, delay: number }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ delay }}
    whileHover={{ y: -5, scale: 1.02 }}
    className="glass p-8 rounded-2xl group hover:border-teal-500/50 transition-all duration-300 relative overflow-hidden h-full"
  >
    <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
      <Icon className="w-24 h-24 text-teal-500" />
    </div>
    <div className="w-12 h-12 bg-teal-500/10 rounded-xl flex items-center justify-center text-teal-400 mb-6 group-hover:scale-110 group-hover:bg-teal-500 group-hover:text-white transition-all duration-300">
      <Icon className="w-6 h-6" />
    </div>
    <h3 className="text-xl font-bold mb-3 text-white">{title}</h3>
    <p className="text-gray-400 leading-relaxed text-sm">
      {description}
    </p>
  </motion.div>
);

const Home = () => {
  const features = [
    {
      icon: Shield,
      title: "NIST SP 800-88 Compliance",
      description: "Supports Clear, Purge, and Destroy methods to ensure full compliance with government and enterprise standards."
    },
    {
      icon: EyeOff,
      title: "Sector-Level Wiping",
      description: "Permanently wipes data from HPA, DCO, and SSD hidden areas where standard tools often fail to reach."
    },
    {
      icon: CloudLightning,
      title: "Bootable Offline Execution",
      description: "Wipe entire systems without an OS. Boot from USB/ISO for low-level hardware access and total destruction."
    },
    {
      icon: FileText,
      title: "Tamper-Proof Certificates",
      description: "Generate cryptographically signed PDF and JSON wipe certificates for audit trails and compliance verification."
    },
    {
      icon: Zap,
      title: "One-Click UI",
      description: "Designed for simplicity. A powerful enterprise tool with a consumer-grade interface for non-technical users."
    },
    {
      icon: Server,
      title: "Enterprise Scalability",
      description: "Manage multiple drives and parallel wiping processes across local or network-connected storage devices."
    }
  ];

  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center pt-20 overflow-hidden">
        {/* Background Gradients */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-teal-500/20 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-[120px] animate-pulse delay-700" />
        
        <div className="container mx-auto px-6 relative z-10 text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
            className="inline-flex items-center gap-2 px-4 py-2 glass rounded-full mb-8 border-teal-500/20"
          >
            <Shield className="w-4 h-4 text-teal-400" />
            <span className="text-sm font-medium text-teal-400 tracking-wide uppercase">The Gold Standard in Data Wiping</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-5xl md:text-7xl font-bold mb-8 tracking-tight leading-tight"
          >
            Secure. Verified.<br />
            <span className="glow-text">Irreversible</span> Data Destruction
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-xl text-gray-400 max-w-2xl mx-auto mb-12 leading-relaxed"
          >
            Based on NIST SP 800-88 standards. ZeroTrace permanently wipes data from SSDs, HDDs, and hidden sectors, making recovery impossible.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="flex flex-col md:flex-row items-center justify-center gap-6"
          >
            <a href="#download" className="btn-primary px-8 py-4 text-lg">
              <Download className="w-5 h-5" />
              Download Now
            </a>
            <button className="btn-secondary px-8 py-4 text-lg">
              Get Started
              <ArrowRight className="w-5 h-5" />
            </button>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1, duration: 1.5 }}
            className="mt-20 flex flex-wrap items-center justify-center gap-12 opacity-50 grayscale hover:grayscale-0 transition-all duration-500"
          >
            <span className="text-white/40 text-sm font-semibold tracking-[0.2em] uppercase">Trusted by Global Enterprises</span>
            {/* Logos could go here */}
          </motion.div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-24 relative overflow-hidden bg-white/[0.02]">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="space-y-8"
            >
              <h2 className="text-4xl font-bold leading-tight">
                Why Standard Deletion <br />
                <span className="text-teal-500">Is Not Safe Enough</span>
              </h2>
              <p className="text-gray-400 text-lg leading-relaxed">
                When you delete a file, your OS only removes the reference. The actual data remains until overwritten. Cybercriminals and data recovery tools can easily retrieve "deleted" files.
              </p>
              <ul className="space-y-4">
                {[
                  "Trust through verifiable transparency",
                  "Compliance with global data security standards",
                  "Protection against corporate espionage",
                  "Bootable USB/ISO wiping for total system reset",
                  "Tamper-proof certificates for compliance audits"
                ].map((item, idx) => (
                  <li key={idx} className="flex items-center gap-3 text-gray-300">
                    <CheckCircle2 className="w-5 h-5 text-teal-500 flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="absolute inset-0 bg-teal-500/10 blur-[80px] rounded-full" />
              <div className="glass aspect-video rounded-3xl border border-white/10 relative overflow-hidden flex items-center justify-center">
                <Shield className="w-48 h-48 text-teal-500/20" />
                <div className="absolute inset-0 bg-gradient-to-tr from-teal-500/5 to-transparent" />
                <div className="p-8 text-center space-y-4">
                    <Cpu className="w-12 h-12 text-teal-500 mx-auto" />
                    <p className="font-mono text-teal-400 text-sm tracking-widest animate-pulse">SYSTEM SECURED</p>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 relative">
        <div className="container mx-auto px-6">
          <div className="text-center mb-20">
            <h2 className="text-4xl font-bold mb-6">Enterprise-Grade <span className="text-teal-500">Security Features</span></h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              ZeroTrace provides the most comprehensive data wiping suite designed for modern hardware and stringent compliance requirements.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, idx) => (
              <FeatureCard key={idx} {...feature} delay={idx * 0.1} />
            ))}
          </div>
        </div>
      </section>

      {/* Download Section */}
      <section id="download" className="py-24 bg-white/[0.02] border-y border-white/5 relative overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[300px] bg-teal-500/10 blur-[100px] rounded-full" />
        <div className="container mx-auto px-6 relative z-10 text-center">
          <h2 className="text-4xl font-bold mb-8">Ready to Secure Your Data?</h2>
          <div className="glass max-w-4xl mx-auto p-12 rounded-[40px] border border-white/10">
            <div className="flex flex-col md:flex-row items-center justify-between gap-12">
              <div className="text-left">
                <h3 className="text-2xl font-bold mb-4">ZeroTrace Desktop v1.0.0</h3>
                <div className="space-y-2 text-gray-400 text-sm">
                  <p>Compatible with: Windows 10/11 (x64), Linux</p>
                  <p>Format: .exe / .iso / .zip</p>
                  <p>Size: ~120 MB</p>
                </div>
              </div>
              <div className="flex flex-col gap-4 w-full md:w-auto">
                <button className="btn-primary px-12 py-5 text-xl">
                  <Download className="w-6 h-6" />
                  Download ZeroTrace
                </button>
                <p className="text-gray-500 text-xs">By downloading, you agree to our Terms of Service.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
