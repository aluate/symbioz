import { NextRequest, NextResponse } from 'next/server';
import { readFile, writeFile } from 'fs/promises';
import { join } from 'path';
import { generateProposal } from '@/factory/proposal/generateProposal';
import { BusinessIntakeSchema } from '@/factory/schemas/intake';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const leadId = searchParams.get('leadId');
    
    if (!leadId) {
      return NextResponse.json(
        { error: 'leadId query parameter required' },
        { status: 400 }
      );
    }

    // Load intake.json
    const intakePath = join(process.cwd(), 'leads', leadId, 'intake.json');
    const intakeData = JSON.parse(await readFile(intakePath, 'utf-8'));
    
    // Validate
    const validated = BusinessIntakeSchema.parse(intakeData);
    
    // Generate proposal
    const proposal = generateProposal(validated);
    
    // Save proposal
    const proposalPath = join(process.cwd(), 'leads', leadId, 'proposal.md');
    await writeFile(proposalPath, proposal);
    
    return NextResponse.json({
      success: true,
      proposal,
      leadId
    });
  } catch (error: any) {
    console.error('Preview error:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: error.message || 'Failed to generate proposal' 
      },
      { status: 500 }
    );
  }
}
