'use client';

import React, { useState } from 'react';

interface Contact {
  phone?: string;
  email?: string;
  address?: string;
  preferredContactMethod?: string;
  hours?: string;
}

interface ContactFormSimpleProps {
  contact: Contact;
}

export default function ContactFormSimple({ contact }: ContactFormSimpleProps) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // In production, this would submit to an API
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 3000);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <section className="py-16 px-4 bg-background">
      <div className="max-w-2xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          <div>
            <h2 className="text-3xl font-semibold text-text mb-6">Get in touch</h2>
            <p className="text-text/80 mb-6">
              Have a question? We're here to help. Reach out and we'll respond as soon as we can.
            </p>
            
            {contact.phone && (
              <div className="mb-4">
                <p className="font-semibold text-text mb-1">Phone</p>
                <a href={`tel:${contact.phone}`} className="text-primary hover:underline">
                  {contact.phone}
                </a>
              </div>
            )}
            
            {contact.email && (
              <div className="mb-4">
                <p className="font-semibold text-text mb-1">Email</p>
                <a href={`mailto:${contact.email}`} className="text-primary hover:underline">
                  {contact.email}
                </a>
              </div>
            )}
            
            {contact.address && (
              <div className="mb-4">
                <p className="font-semibold text-text mb-1">Address</p>
                <p className="text-text/80">{contact.address}</p>
              </div>
            )}
            
            {contact.hours && (
              <div>
                <p className="font-semibold text-text mb-1">Hours</p>
                <p className="text-text/80">{contact.hours}</p>
              </div>
            )}
          </div>

          <div>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-text font-medium mb-2">
                  Name
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-mutedSurface rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>
              
              <div>
                <label htmlFor="email" className="block text-text font-medium mb-2">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-mutedSurface rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>
              
              <div>
                <label htmlFor="message" className="block text-text font-medium mb-2">
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows={5}
                  className="w-full px-4 py-2 border border-mutedSurface rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>
              
              <button
                type="submit"
                className="w-full bg-primary text-white px-8 py-3 rounded-lg font-medium hover:opacity-90 transition"
              >
                {submitted ? 'Message sent' : 'Send message'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}

