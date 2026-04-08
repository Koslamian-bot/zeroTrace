import React from 'react';
import { motion } from 'framer-motion';
import { Shield, Mail, Lock, User, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

const Signup = () => {
  return (
    <div className="min-h-screen pt-24 pb-12 flex items-center justify-center relative overflow-hidden">
      {/* Background Blobs */}
      <div className="absolute top-1/4 left-1/3 w-64 h-64 bg-teal-500/10 rounded-full blur-[100px]" />
      <div className="absolute bottom-1/4 right-1/3 w-64 h-64 bg-cyan-500/10 rounded-full blur-[100px]" />

      <motion.div
        initial={{ opacity: 0, scale: 0.9, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="container mx-auto px-6 relative z-10"
      >
        <div className="glass max-w-md mx-auto p-10 rounded-[32px] border border-white/10 shadow-2xl">
          <div className="text-center mb-10">
            <Link to="/" className="inline-flex items-center gap-2 mb-6 group">
              <Shield className="w-10 h-10 text-teal-500 group-hover:rotate-12 transition-transform" />
              <span className="text-2xl font-bold text-white tracking-wider">ZeroTrace</span>
            </Link>
            <h2 className="text-3xl font-bold mb-2">Create Account</h2>
            <p className="text-gray-400">Join the elite cybersecurity community</p>
          </div>

          <form className="space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300 ml-1">Full Name</label>
              <div className="relative group">
                <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500 group-focus-within:text-teal-500 transition-colors" />
                <input
                  type="text"
                  placeholder="John Doe"
                  className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-white placeholder-gray-600 focus:outline-none focus:border-teal-500/50 focus:ring-4 focus:ring-teal-500/10 transition-all"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300 ml-1">Email Address</label>
              <div className="relative group">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500 group-focus-within:text-teal-500 transition-colors" />
                <input
                  type="email"
                  placeholder="name@company.com"
                  className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-white placeholder-gray-600 focus:outline-none focus:border-teal-500/50 focus:ring-4 focus:ring-teal-500/10 transition-all"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300 ml-1">Password</label>
              <div className="relative group">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500 group-focus-within:text-teal-500 transition-colors" />
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-white placeholder-gray-600 focus:outline-none focus:border-teal-500/50 focus:ring-4 focus:ring-teal-500/10 transition-all"
                />
              </div>
            </div>

            <Link to="/dashboard" className="btn-primary w-full py-4 text-lg mt-4 group">
              Create Account
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
          </form>

          <div className="mt-10 text-center">
            <p className="text-gray-400">
              Already have an account?{' '}
              <Link to="/login" className="text-teal-500 hover:text-teal-400 font-semibold transition-colors">Login here</Link>
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Signup;
