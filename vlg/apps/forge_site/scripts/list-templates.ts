#!/usr/bin/env node

/**
 * Forge Site — List Templates
 * 
 * Lists available templates with descriptions and use cases.
 */

import * as fs from 'fs';
import * as path from 'path';

function listTemplates(): void {
  const templateIndexPath = path.join(__dirname, '..', 'data', 'template_index.json');

  if (!fs.existsSync(templateIndexPath)) {
    console.error('❌ Template index not found');
    process.exit(1);
  }

  const templateIndex = JSON.parse(fs.readFileSync(templateIndexPath, 'utf-8'));

  console.log('📋 Available Templates\n');

  templateIndex.templates.forEach((template: any) => {
    console.log(`🔹 ${template.name} (${template.id})`);
    console.log(`   ${template.description}`);
    console.log(`   Target Industries: ${template.targetIndustries.join(', ')}`);
    console.log(`   Primary Goals: ${template.primaryGoal.join(', ')}`);
    console.log(`   Pages: ${template.defaultPages.join(', ')}`);
    console.log('');
  });
}

listTemplates();

