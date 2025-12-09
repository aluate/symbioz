#!/usr/bin/env node

/**
 * Forge Site — Generate Brand From Input
 * 
 * Takes raw brand input (conversation, intake form, notes) and generates
 * a complete brand system with colors, typography, and voice guidelines.
 */

import * as fs from 'fs';
import * as path from 'path';

interface BrandInput {
  brandPersonality?: string[];
  brandFeel?: string;
  brandNeverFeel?: string;
  visualStyle?: string;
  coreBeliefs?: string;
  colorPreferences?: {
    loved?: string[];
    hated?: string[];
  };
  toneOfVoice?: string;
  wordsToAvoid?: string[];
  visualReferences?: string[];
  conversationTranscript?: string;
  notes?: string;
}

interface BrandTokens {
  brandName: string;
  personality: string[];
  brandFeel: string;
  brandNeverFeel: string;
  coreBeliefs: string[];
  colors: {
    primary: { hex: string; name: string; usage: string };
    secondary: { hex: string; name: string; usage: string };
    background: { hex: string; name: string; usage: string };
    text: { hex: string; name: string; usage: string };
    accent?: { hex: string; name: string; usage: string };
  };
  typography: {
    fontFamily: {
      primary: string;
      stack: string[];
    };
    headings: {
      h1: { size: string; lineHeight: string; weight: number };
      h2: { size: string; lineHeight: string; weight: number };
      h3: { size: string; lineHeight: string; weight: number };
      h4: { size: string; lineHeight: string; weight: number };
    };
    body: {
      size: string;
      lineHeight: string;
      weight: number;
    };
  };
  voice: {
    tone: string;
    style: string;
    wordsToUse: string[];
    wordsToAvoid: string[];
    examples: string[];
  };
  spacing: {
    baseUnit: number;
    scale: number[];
  };
  visualStyle: {
    references: string[];
    notes: string;
  };
}

function generateColorsFromPersonality(
  personality: string[],
  feel: string,
  neverFeel: string,
  colorPrefs?: { loved?: string[]; hated?: string[] }
): BrandTokens['colors'] {
  // Simple color generation based on personality and preferences
  // In production, this would use AI/LLM for sophisticated palette generation

  const personalityStr = personality.join(' ').toLowerCase();
  const feelStr = feel.toLowerCase();
  const neverStr = neverFeel.toLowerCase();

  // Default palette (Forge Site defaults)
  let primary = { hex: '#5D7586', name: 'Steel Blue', usage: 'Primary brand color' };
  let secondary = { hex: '#F4F2EC', name: 'Porcelain', usage: 'Background color' };
  let background = { hex: '#F4F2EC', name: 'Porcelain', usage: 'Page background' };
  let text = { hex: '#2F3136', name: 'Graphite', usage: 'Primary text' };
  let accent: { hex: string; name: string; usage: string } | undefined;

  // Personality-based color selection
  if (personalityStr.includes('rugged') || personalityStr.includes('reliable') || personalityStr.includes('solid')) {
    // Earth tones, deep browns, warm grays
    primary = { hex: '#6B5B4F', name: 'Deep Brown', usage: 'Primary brand color' };
    secondary = { hex: '#D4C5B9', name: 'Warm Gray', usage: 'Supporting color' };
    background = { hex: '#F5F1ED', name: 'Cream', usage: 'Page background' };
    text = { hex: '#2C2416', name: 'Charcoal', usage: 'Primary text' };
  } else if (personalityStr.includes('creative') || personalityStr.includes('bold') || personalityStr.includes('innovative')) {
    // Vibrant, modern colors
    primary = { hex: '#4A90E2', name: 'Vibrant Blue', usage: 'Primary brand color' };
    secondary = { hex: '#F39C12', name: 'Accent Orange', usage: 'Supporting color' };
    background = { hex: '#FFFFFF', name: 'White', usage: 'Page background' };
    text = { hex: '#1A1A1A', name: 'Near Black', usage: 'Primary text' };
    accent = { hex: '#E74C3C', name: 'Accent Red', usage: 'Highlights and CTAs' };
  } else if (personalityStr.includes('calm') || personalityStr.includes('peaceful') || personalityStr.includes('soothing')) {
    // Muted, soft colors
    primary = { hex: '#7FB3D3', name: 'Soft Blue', usage: 'Primary brand color' };
    secondary = { hex: '#A8C5A0', name: 'Sage Green', usage: 'Supporting color' };
    background = { hex: '#FAF9F7', name: 'Warm White', usage: 'Page background' };
    text = { hex: '#3D3D3D', name: 'Soft Charcoal', usage: 'Primary text' };
  } else if (personalityStr.includes('professional') || personalityStr.includes('formal') || personalityStr.includes('serious')) {
    // Neutral, professional colors
    primary = { hex: '#2C3E50', name: 'Navy', usage: 'Primary brand color' };
    secondary = { hex: '#95A5A6', name: 'Slate Gray', usage: 'Supporting color' };
    background = { hex: '#FFFFFF', name: 'White', usage: 'Page background' };
    text = { hex: '#1A1A1A', name: 'Black', usage: 'Primary text' };
  }

  // Override with explicit color preferences if provided
  if (colorPrefs?.loved && colorPrefs.loved.length > 0) {
    // In production, parse color names/hex codes and use them
    // For now, just note that preferences exist
  }

  // Avoid hated colors (ensure they're not in palette)
  if (colorPrefs?.hated && colorPrefs.hated.length > 0) {
    // In production, check palette against hated colors and adjust
  }

  return {
    primary,
    secondary,
    background,
    text,
    ...(accent && { accent }),
  };
}

function generateTypographyFromPersonality(
  personality: string[],
  feel: string
): BrandTokens['typography'] {
  const personalityStr = personality.join(' ').toLowerCase();
  const feelStr = feel.toLowerCase();

  let fontFamily = 'Inter';
  let fontStack = ['Inter', 'system-ui', '-apple-system', 'sans-serif'];

  if (personalityStr.includes('professional') || personalityStr.includes('formal')) {
    fontFamily = 'Playfair Display';
    fontStack = ['Playfair Display', 'Georgia', 'serif'];
  } else if (personalityStr.includes('modern') || personalityStr.includes('clean')) {
    fontFamily = 'Inter';
    fontStack = ['Inter', 'system-ui', '-apple-system', 'sans-serif'];
  } else if (personalityStr.includes('friendly') || personalityStr.includes('warm')) {
    fontFamily = 'Plus Jakarta Sans';
    fontStack = ['Plus Jakarta Sans', 'system-ui', '-apple-system', 'sans-serif'];
  } else if (personalityStr.includes('creative') || personalityStr.includes('bold')) {
    fontFamily = 'Work Sans';
    fontStack = ['Work Sans', 'system-ui', '-apple-system', 'sans-serif'];
  }

  return {
    fontFamily: {
      primary: fontFamily,
      stack: fontStack,
    },
    headings: {
      h1: { size: '3rem', lineHeight: '1.25', weight: 700 },
      h2: { size: '2.25rem', lineHeight: '1.375', weight: 600 },
      h3: { size: '1.875rem', lineHeight: '1.5', weight: 600 },
      h4: { size: '1.5rem', lineHeight: '1.5', weight: 500 },
    },
    body: {
      size: '1rem',
      lineHeight: '1.625',
      weight: 400,
    },
  };
}

function generateVoiceFromInput(
  toneOfVoice?: string,
  wordsToAvoid?: string[],
  brandFeel?: string,
  brandNeverFeel?: string
): BrandTokens['voice'] {
  const tone = toneOfVoice || 'Professional but friendly';
  const style = brandFeel || 'Clear and direct';

  const wordsToUse: string[] = [];
  const wordsToAvoidList = wordsToAvoid || [];
  const examples: string[] = [];

  // Generate examples based on tone
  if (tone.includes('professional')) {
    wordsToUse.push('quality', 'expertise', 'reliable', 'professional');
    examples.push('We deliver quality results on time.');
  }
  if (tone.includes('friendly')) {
    wordsToUse.push('welcome', 'help', 'support', 'friendly');
    examples.push('We're here to help you succeed.');
  }
  if (tone.includes('direct')) {
    wordsToUse.push('clear', 'straightforward', 'honest', 'direct');
    examples.push('We tell it straight. No fluff.');
  }
  if (tone.includes('creative')) {
    wordsToUse.push('innovative', 'creative', 'unique', 'bold');
    examples.push('We bring fresh ideas to every project.');
  }

  return {
    tone,
    style,
    wordsToUse,
    wordsToAvoid: wordsToAvoidList,
    examples,
  };
}

function generateBrandTokens(
  businessName: string,
  input: BrandInput
): BrandTokens {
  const personality = input.brandPersonality || ['professional', 'reliable', 'clear'];
  const feel = input.brandFeel || 'Professional and trustworthy';
  const neverFeel = input.brandNeverFeel || 'Corporate or flashy';
  const coreBeliefs = input.coreBeliefs
    ? [input.coreBeliefs]
    : ['Quality work matters', 'Honest communication'];

  const colors = generateColorsFromPersonality(
    personality,
    feel,
    neverFeel,
    input.colorPreferences
  );

  const typography = generateTypographyFromPersonality(personality, feel);

  const voice = generateVoiceFromInput(
    input.toneOfVoice,
    input.wordsToAvoid,
    feel,
    neverFeel
  );

  return {
    brandName: businessName,
    personality,
    brandFeel: feel,
    brandNeverFeel: neverFeel,
    coreBeliefs,
    colors,
    typography,
    voice,
    spacing: {
      baseUnit: 8,
      scale: [8, 16, 24, 32, 40, 48, 64, 80, 96],
    },
    visualStyle: {
      references: input.visualReferences || [],
      notes: input.visualStyle || '',
    },
  };
}

function parseBrandInput(inputPath: string): BrandInput {
  if (!fs.existsSync(inputPath)) {
    throw new Error(`Input file not found: ${inputPath}`);
  }

  const content = fs.readFileSync(inputPath, 'utf-8');

  // Try to parse as JSON first
  try {
    const json = JSON.parse(content);
    return json as BrandInput;
  } catch {
    // If not JSON, treat as plain text
    // In production, this would use AI/LLM to extract structured data
    // For now, return a basic structure
    return {
      notes: content,
      conversationTranscript: content,
    };
  }
}

function generateBrandFromInput(
  inputPath: string,
  businessName: string,
  outputPath: string
): void {
  console.log('🎨 Forge Site Brand Generator\n');

  // Parse input
  console.log(`📖 Reading input: ${inputPath}`);
  const input = parseBrandInput(inputPath);

  // Generate brand tokens
  console.log('✨ Generating brand system...');
  const tokens = generateBrandTokens(businessName, input);

  // Save output
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(outputPath, JSON.stringify(tokens, null, 2));
  console.log(`✅ Brand tokens saved: ${outputPath}`);

  // Print summary
  console.log('\n📋 Brand System Summary:');
  console.log(`   Personality: ${tokens.personality.join(', ')}`);
  console.log(`   Feel: ${tokens.brandFeel}`);
  console.log(`   Never Feel: ${tokens.brandNeverFeel}`);
  console.log(`   Primary Color: ${tokens.colors.primary.name} (${tokens.colors.primary.hex})`);
  console.log(`   Typography: ${tokens.typography.fontFamily.primary}`);
  console.log(`   Tone: ${tokens.voice.tone}`);
}

// CLI entry point
const args = process.argv.slice(2);
if (args.length < 3) {
  console.error('Usage: generate-brand-from-input.ts <input-path> <business-name> <output-path>');
  console.error('Example: generate-brand-from-input.ts brand-input.txt "Acme Builders" output/brand-tokens.json');
  process.exit(1);
}

const [inputPath, businessName, outputPath] = args;
generateBrandFromInput(inputPath, businessName, outputPath);

