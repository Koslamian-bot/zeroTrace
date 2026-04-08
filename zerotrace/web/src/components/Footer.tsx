import React from 'react';
import { Shield, Twitter, Github, Linkedin, Mail } from 'lucide-react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-[#050505] border-t border-white/5 py-16">
      <div className="container mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
          {/* Logo and About */}
          <div className="md:col-span-2">
            <Link to="/" className="flex items-center gap-2 mb-6">
              <Shield className="w-8 h-8 text-teal-500" />
              <span className="text-xl font-bold text-white tracking-wider uppercase">ZeroTrace</span>
            </Link>
            <p className="text-gray-400 max-w-sm mb-8">
              The gold standard in secure data destruction. NIST SP 800-88 compliant, enterprise-ready, and irreversibly secure.
            </p>
            <div className="flex gap-4">
              {[Twitter, Github, Linkedin, Mail].map((Icon, idx) => (
                <a
                  key={idx}
                  href="#"
                  className="w-10 h-10 rounded-full glass flex items-center justify-center text-gray-400 hover:text-teal-400 hover:border-teal-400/50 transition-all duration-300"
                >
                  <Icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>

          {/* Links */}
          <div>
            <h4 className="text-white font-semibold mb-6">Product</h4>
            <ul className="space-y-4">
              <li><a href="#features" className="text-gray-400 hover:text-teal-400 transition-colors">Features</a></li>
              <li><a href="#download" className="text-gray-400 hover:text-teal-400 transition-colors">Download</a></li>
              <li><a href="#" className="text-gray-400 hover:text-teal-400 transition-colors">Compliance</a></li>
              <li><a href="#" className="text-gray-400 hover:text-teal-400 transition-colors">Pricing</a></li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h4 className="text-white font-semibold mb-6">Company</h4>
            <ul className="space-y-4">
              <li><a href="#about" className="text-gray-400 hover:text-teal-400 transition-colors">About Us</a></li>
              <li><a href="#" className="text-gray-400 hover:text-teal-400 transition-colors">Contact</a></li>
              <li><a href="#" className="text-gray-400 hover:text-teal-400 transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="text-gray-400 hover:text-teal-400 transition-colors">Terms of Service</a></li>
            </ul>
          </div>
        </div>

        <div className="mt-16 pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-gray-500 text-sm">
            © {new Date().getFullYear()} ZeroTrace Security Solutions. All rights reserved.
          </p>
          <div className="flex gap-8 text-sm text-gray-500">
            <span>Made with ❤️ for SIH 2024</span>
            <span>Version 1.0.0</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
