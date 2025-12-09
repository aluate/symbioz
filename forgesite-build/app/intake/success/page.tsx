'use client';

import { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

function SuccessContent() {
  const searchParams = useSearchParams();
  const leadId = searchParams.get('leadId');

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="max-w-2xl mx-auto text-center bg-white p-12 rounded-lg shadow-md">
        <div className="text-6xl mb-6">✓</div>
        <h1 className="text-4xl font-bold mb-4">Factory Run Queued</h1>
        <p className="text-lg text-gray-600 mb-4">
          Your website factory run has been queued. We'll review your intake, generate a plan, and send a proposal outlining your build and launch timeline.
        </p>
        <p className="text-sm text-gray-500 mb-8">
          Most sites go live within 3-7 days of intake approval and payment.
        </p>
        {leadId && (
          <p className="text-sm text-gray-500 mb-8">
            Lead ID: <code className="bg-gray-100 px-2 py-1 rounded">{leadId}</code>
          </p>
        )}
        <div className="space-y-4">
          <Button asChild className="bg-blue-600 hover:bg-blue-700">
            <Link href="/">Back to Home</Link>
          </Button>
        </div>
      </div>
    </div>
  );
}

export default function IntakeSuccessPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SuccessContent />
    </Suspense>
  );
}
