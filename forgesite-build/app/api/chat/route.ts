import { NextRequest, NextResponse } from 'next/server';

// This is a foundation - will be enhanced with actual AI later
export async function POST(request: NextRequest) {
  try {
    const { message, leadId } = await request.json();
    
    if (!message) {
      return NextResponse.json(
        { error: 'Message is required' },
        { status: 400 }
      );
    }
    
    // Factory Assistant - rule-based responses for v1
    // Future: Integrate with AI model trained on Karl's voice
    
    const responses: Record<string, string> = {
      'change service': 'I can help update your services list. What needs to change?',
      'update phone': 'I\'ll update your phone number. What\'s the new number?',
      'swap photo': 'Which project photo would you like to replace?',
      'add testimonial': 'Great! Send me the testimonial text and the person\'s name.',
      'change headline': 'Which page and which headline? I\'ll update it.',
      'update email': 'I\'ll update your email address. What\'s the new email?',
      'change address': 'I can update your address. What\'s the new address?',
      'redesign': 'That\'s a bigger change than a config tweak. Major layout or design changes require a new factory run or package upgrade. I can log this request for review.',
      'custom design': 'We\'re a website factory, so we work from proven layouts instead of designing from scratch. Custom design work requires a new factory run. What specifically do you need?',
      'more pages': 'Additional pages outside your package require a new factory run or package upgrade. I can log this request for review.',
      'help': 'I\'m the Factory Assistant. I can help with small config changes to your site like updating services, contact info, headlines, or adding testimonials. For bigger changes, I can log a new factory run request. What would you like to change?',
    };
    
    // Simple keyword matching (v1)
    const lowerMessage = message.toLowerCase();
    const matchedKey = Object.keys(responses).find(key => 
      lowerMessage.includes(key.split(' ')[0])
    );
    
    // Check for big change requests that need escalation
    const bigChangeKeywords = ['redesign', 'custom design', 'new layout', 'completely different', 'start over', 'rebuild'];
    const isBigChange = bigChangeKeywords.some(keyword => lowerMessage.includes(keyword));
    
    let response: string;
    if (isBigChange) {
      response = 'That\'s a bigger change than a config tweak. Major layout or design changes require a new factory run or package upgrade. I can log this request for review. What specifically do you need changed?';
    } else if (matchedKey) {
      response = responses[matchedKey];
    } else {
      response = 'I\'m the Factory Assistant. I can help with small config changes to your site like updating services, contact info, headlines, or adding testimonials. For bigger changes, I can log a new factory run request. What would you like to change?';
    }
    
    return NextResponse.json({
      success: true,
      response,
      leadId: leadId || null
    });
  } catch (error: any) {
    console.error('Chat error:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: error.message || 'Failed to process chat message' 
      },
      { status: 500 }
    );
  }
}
