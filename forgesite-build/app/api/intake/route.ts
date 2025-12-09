import { NextRequest, NextResponse } from 'next/server';
import { BusinessIntakeSchema } from '@/factory/schemas/intake';
import { writeFile, mkdir } from 'fs/promises';
import { join } from 'path';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validated = BusinessIntakeSchema.parse(body);
    
    // Generate unique ID
    const leadId = `${Date.now()}-${validated.businessName.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')}`;
    
    // Save to /leads/{leadId}/intake.json
    const leadsDir = join(process.cwd(), 'leads', leadId);
    await mkdir(leadsDir, { recursive: true });
    await writeFile(
      join(leadsDir, 'intake.json'),
      JSON.stringify(validated, null, 2)
    );
    
    return NextResponse.json({
      success: true,
      leadId,
      message: 'Intake received. We\'ll build your site preview shortly.'
    });
  } catch (error: any) {
    console.error('Intake error:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: error.message || 'Invalid intake data' 
      },
      { status: 400 }
    );
  }
}
