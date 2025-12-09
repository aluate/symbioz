'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { BusinessIntakeSchema } from '@/factory/schemas/intake';

export default function IntakePage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    businessName: '',
    ownerName: '',
    tradeType: 'builder' as const,
    serviceArea: '',
    services: [''],
    typicalJobSize: '',
    idealClientDescription: '',
    differentiators: [''],
    mainGoal: 'get_leads' as const,
    brandVoice: 'straightforward' as const,
    packageLevel: 'basic' as const,
    contact: {
      phone: '',
      email: '',
      address: ''
    }
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    try {
      // Clean up empty strings from arrays
      const cleanedData = {
        ...formData,
        services: formData.services.filter(s => s.trim() !== ''),
        differentiators: formData.differentiators.filter(d => d.trim() !== ''),
        ownerName: formData.ownerName || undefined,
        typicalJobSize: formData.typicalJobSize || undefined,
        idealClientDescription: formData.idealClientDescription || undefined,
        contact: {
          ...formData.contact,
          address: formData.contact.address || undefined
        }
      };

      // Validate with Zod
      const validated = BusinessIntakeSchema.parse(cleanedData);

      // Submit to API
      const response = await fetch('/api/intake', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(validated)
      });

      const result = await response.json();

      if (result.success) {
        router.push(`/intake/success?leadId=${result.leadId}`);
      } else {
        setError(result.error || 'Failed to submit intake');
      }
    } catch (err: any) {
      setError(err.message || 'Validation failed');
    } finally {
      setSubmitting(false);
    }
  };

  const addService = () => {
    setFormData(prev => ({
      ...prev,
      services: [...prev.services, '']
    }));
  };

  const updateService = (idx: number, value: string) => {
    setFormData(prev => ({
      ...prev,
      services: prev.services.map((s, i) => i === idx ? value : s)
    }));
  };

  const addDifferentiator = () => {
    setFormData(prev => ({
      ...prev,
      differentiators: [...prev.differentiators, '']
    }));
  };

  const updateDifferentiator = (idx: number, value: string) => {
    setFormData(prev => ({
      ...prev,
      differentiators: prev.differentiators.map((d, i) => i === idx ? value : d)
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50 py-16 px-4">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center">Start a Website Factory Run</h1>
        <p className="text-center text-gray-600 mb-8">
          Answer a few focused questions about your business. We use this intake to assemble your site from factory-tested modules.
        </p>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md space-y-6">
          {/* Business Info */}
          <div>
            <label className="block text-sm font-medium mb-2">Business Name *</label>
            <Input
              value={formData.businessName}
              onChange={(e) => setFormData(prev => ({ ...prev, businessName: e.target.value }))}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Owner Name</label>
            <Input
              value={formData.ownerName}
              onChange={(e) => setFormData(prev => ({ ...prev, ownerName: e.target.value }))}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Trade Type *</label>
            <select
              value={formData.tradeType}
              onChange={(e) => setFormData(prev => ({ ...prev, tradeType: e.target.value as any }))}
              className="w-full h-10 rounded-md border border-gray-300 px-3"
              required
            >
              <option value="builder">Builder</option>
              <option value="remodeler">Remodeler</option>
              <option value="cabinet_shop">Cabinet Shop</option>
              <option value="steel_buildings">Steel Buildings</option>
              <option value="hvac">HVAC</option>
              <option value="electrical">Electrical</option>
              <option value="plumbing">Plumbing</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Service Area *</label>
            <Input
              value={formData.serviceArea}
              onChange={(e) => setFormData(prev => ({ ...prev, serviceArea: e.target.value }))}
              required
            />
          </div>

          {/* Services */}
          <div>
            <label className="block text-sm font-medium mb-2">Services *</label>
            <p className="text-sm text-gray-500 mb-2">List the main services you actually sell. We'll turn this into clear sections on your site.</p>
            {formData.services.map((service, idx) => (
              <Input
                key={idx}
                value={service}
                onChange={(e) => updateService(idx, e.target.value)}
                placeholder="Service name"
                className="mb-2"
                required={idx === 0}
              />
            ))}
            <Button type="button" variant="outline" onClick={addService} className="mt-2">
              + Add Service
            </Button>
          </div>

          {/* Contact */}
          <div>
            <label className="block text-sm font-medium mb-2">Phone *</label>
            <Input
              type="tel"
              value={formData.contact.phone}
              onChange={(e) => setFormData(prev => ({
                ...prev,
                contact: { ...prev.contact, phone: e.target.value }
              }))}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Email *</label>
            <Input
              type="email"
              value={formData.contact.email}
              onChange={(e) => setFormData(prev => ({
                ...prev,
                contact: { ...prev.contact, email: e.target.value }
              }))}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Address</label>
            <Input
              value={formData.contact.address}
              onChange={(e) => setFormData(prev => ({
                ...prev,
                contact: { ...prev.contact, address: e.target.value }
              }))}
            />
          </div>

          {/* Goals */}
          <div>
            <label className="block text-sm font-medium mb-2">Main Goal *</label>
            <select
              value={formData.mainGoal}
              onChange={(e) => setFormData(prev => ({ ...prev, mainGoal: e.target.value as any }))}
              className="w-full h-10 rounded-md border border-gray-300 px-3"
              required
            >
              <option value="get_leads">Get Leads</option>
              <option value="look_legit">Look Legitimate</option>
              <option value="recruit_staff">Recruit Staff</option>
              <option value="showcase_projects">Showcase Projects</option>
            </select>
          </div>

          {/* Package */}
          <div>
            <label className="block text-sm font-medium mb-2">Package Level *</label>
            <select
              value={formData.packageLevel}
              onChange={(e) => setFormData(prev => ({ ...prev, packageLevel: e.target.value as any }))}
              className="w-full h-10 rounded-md border border-gray-300 px-3"
              required
            >
              <option value="basic">Starter Run - $1,495</option>
              <option value="pro">Workhorse Run - $2,950</option>
              <option value="premium">Premium Run - $6,950</option>
            </select>
          </div>

          {/* Optional Fields */}
          <div>
            <label className="block text-sm font-medium mb-2">Typical Job Size</label>
            <Input
              value={formData.typicalJobSize}
              onChange={(e) => setFormData(prev => ({ ...prev, typicalJobSize: e.target.value }))}
              placeholder="e.g., $50,000 - $200,000"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Ideal Client Description</label>
            <Textarea
              value={formData.idealClientDescription}
              onChange={(e) => setFormData(prev => ({ ...prev, idealClientDescription: e.target.value }))}
              rows={3}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Differentiators</label>
            {formData.differentiators.map((diff, idx) => (
              <Input
                key={idx}
                value={diff}
                onChange={(e) => updateDifferentiator(idx, e.target.value)}
                placeholder="What makes you different"
                className="mb-2"
              />
            ))}
            <Button type="button" variant="outline" onClick={addDifferentiator} className="mt-2">
              + Add Differentiator
            </Button>
          </div>

          <Button 
            type="submit" 
            className="w-full bg-blue-600 hover:bg-blue-700"
            disabled={submitting}
          >
            {submitting ? 'Submitting...' : 'Submit Intake'}
          </Button>
        </form>
      </div>
    </div>
  );
}
