'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

interface LeadCaptureSectionProps {
  title?: string;
  fields?: string[];
  brandColors?: {
    primary?: string;
    secondary?: string;
  };
}

export function LeadCaptureSection({ 
  title = "Get In Touch",
  fields = ['name', 'email', 'phone', 'message'],
  brandColors 
}: LeadCaptureSectionProps) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: ''
  });
  const primaryColor = brandColors?.primary || 'bg-blue-600';

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Form submission logic here
    console.log('Form submitted:', formData);
  };

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <section className="py-16 px-4 bg-gray-50">
      <div className="max-w-2xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-8">{title}</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          {fields.includes('name') && (
            <div>
              <label htmlFor="name" className="block text-sm font-medium mb-2">
                Name
              </label>
              <Input
                id="name"
                type="text"
                value={formData.name}
                onChange={(e) => handleChange('name', e.target.value)}
                required
                className="w-full"
              />
            </div>
          )}
          {fields.includes('email') && (
            <div>
              <label htmlFor="email" className="block text-sm font-medium mb-2">
                Email
              </label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => handleChange('email', e.target.value)}
                required
                className="w-full"
              />
            </div>
          )}
          {fields.includes('phone') && (
            <div>
              <label htmlFor="phone" className="block text-sm font-medium mb-2">
                Phone
              </label>
              <Input
                id="phone"
                type="tel"
                value={formData.phone}
                onChange={(e) => handleChange('phone', e.target.value)}
                className="w-full"
              />
            </div>
          )}
          {fields.includes('message') && (
            <div>
              <label htmlFor="message" className="block text-sm font-medium mb-2">
                Message
              </label>
              <Textarea
                id="message"
                value={formData.message}
                onChange={(e) => handleChange('message', e.target.value)}
                rows={5}
                className="w-full"
              />
            </div>
          )}
          <Button type="submit" className={`w-full ${primaryColor} hover:opacity-90`}>
            Submit
          </Button>
        </form>
      </div>
    </section>
  );
}
