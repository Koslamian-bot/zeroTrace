import React from 'react';
import { motion } from 'framer-motion';
import { 
  CreditCard, 
  Plus, 
  History, 
  ShieldCheck, 
  Zap, 
  LayoutDashboard, 
  Settings, 
  LogOut,
  TrendingUp,
  FileText
} from 'lucide-react';

const Dashboard = () => {
  const plans = [
    {
      name: 'Basic',
      credits: '50 Credits',
      price: '$29',
      features: ['10 Full Wipes', 'Email Support', 'Basic Certificates'],
      color: 'bg-blue-500/10 text-blue-400'
    },
    {
      name: 'Pro',
      credits: '250 Credits',
      price: '$99',
      features: ['50 Full Wipes', 'Priority Support', 'NIST Compliance PDFs', 'API Access'],
      color: 'bg-teal-500/20 text-teal-400 border-teal-500/30',
      recommended: true
    },
    {
      name: 'Enterprise',
      credits: 'Unlimited',
      price: 'Custom',
      features: ['Unlimited Wipes', '24/7 Phone Support', 'Custom Integration', 'On-prem Deployment'],
      color: 'bg-purple-500/10 text-purple-400'
    }
  ];

  return (
    <div className="min-h-screen bg-[#050505] flex pt-20">
      {/* Sidebar */}
      <aside className="w-64 border-r border-white/5 hidden lg:flex flex-col p-6 fixed h-full pt-28">
        <nav className="space-y-2 flex-1">
          {[
            { icon: LayoutDashboard, name: 'Overview', active: true },
            { icon: History, name: 'Wipe History' },
            { icon: CreditCard, name: 'Billing' },
            { icon: FileText, name: 'Certificates' },
            { icon: Settings, name: 'Settings' },
          ].map((item) => (
            <button
              key={item.name}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                item.active ? 'bg-teal-500/10 text-teal-400' : 'text-gray-400 hover:bg-white/5 hover:text-white'
              }`}
            >
              <item.icon className="w-5 h-5" />
              <span className="font-medium">{item.name}</span>
            </button>
          ))}
        </nav>
        <button className="flex items-center gap-3 px-4 py-3 text-red-400 hover:bg-red-400/10 rounded-xl transition-all">
          <LogOut className="w-5 h-5" />
          <span className="font-medium">Logout</span>
        </button>
      </aside>

      {/* Main Content */}
      <main className="flex-1 lg:ml-64 p-8 lg:p-12">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12">
            <div>
              <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
              <p className="text-gray-400">Welcome back, security expert. Manage your credits and wipes.</p>
            </div>
            <div className="glass px-6 py-4 rounded-2xl flex items-center gap-4 border-teal-500/20">
              <div className="w-10 h-10 bg-teal-500/20 rounded-full flex items-center justify-center text-teal-400">
                <Zap className="w-6 h-6" />
              </div>
              <div>
                <p className="text-xs text-gray-400 uppercase tracking-wider font-bold">Current Balance</p>
                <p className="text-xl font-bold text-white">124 Credits</p>
              </div>
              <button className="btn-primary p-2 ml-4">
                <Plus className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            {[
              { label: 'Total Wipes', value: '42', icon: ShieldCheck, trend: '+12% this month' },
              { label: 'Data Destroyed', value: '1.2 TB', icon: TrendingUp, trend: 'Irreversible' },
              { label: 'Active Devices', value: '3', icon: LayoutDashboard, trend: 'Secure connection' },
            ].map((stat, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="glass p-6 rounded-2xl border-white/5"
              >
                <div className="flex justify-between items-start mb-4">
                  <div className="w-12 h-12 bg-white/5 rounded-xl flex items-center justify-center text-gray-400">
                    <stat.icon className="w-6 h-6" />
                  </div>
                  <span className="text-xs text-teal-500 font-medium">{stat.trend}</span>
                </div>
                <p className="text-gray-400 text-sm mb-1">{stat.label}</p>
                <p className="text-3xl font-bold text-white">{stat.value}</p>
              </motion.div>
            ))}
          </div>

          {/* Credits Store */}
          <div className="mb-12">
            <h2 className="text-2xl font-bold mb-8">Purchase Credits</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {plans.map((plan, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.3 + idx * 0.1 }}
                  className={`glass p-8 rounded-3xl relative flex flex-col ${plan.recommended ? 'border-teal-500/50 scale-105 shadow-2xl shadow-teal-500/10' : 'border-white/5'}`}
                >
                  {plan.recommended && (
                    <span className="absolute -top-4 left-1/2 -translate-x-1/2 bg-teal-500 text-white text-xs font-bold px-4 py-1.5 rounded-full uppercase tracking-widest">
                      Best Value
                    </span>
                  )}
                  <div className={`w-fit px-3 py-1 rounded-lg text-xs font-bold uppercase mb-4 ${plan.color}`}>
                    {plan.name}
                  </div>
                  <h3 className="text-3xl font-bold mb-2 text-white">{plan.credits}</h3>
                  <p className="text-gray-400 mb-6"><span className="text-white text-2xl font-bold">{plan.price}</span> / one-time</p>
                  
                  <ul className="space-y-4 mb-10 flex-1">
                    {plan.features.map((feature, fIdx) => (
                      <li key={fIdx} className="flex items-center gap-3 text-sm text-gray-300">
                        <ShieldCheck className="w-4 h-4 text-teal-500" />
                        {feature}
                      </li>
                    ))}
                  </ul>

                  <button className={`w-full py-4 rounded-2xl font-bold transition-all ${
                    plan.recommended ? 'bg-teal-500 hover:bg-teal-400 text-white shadow-lg shadow-teal-500/20' : 'bg-white/5 hover:bg-white/10 text-white'
                  }`}>
                    Buy {plan.name}
                  </button>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
