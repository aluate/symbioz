#!/usr/bin/env node

/**
 * Forge Site — Generate Template
 * 
 * Scaffolds a new base template folder with a config file.
 */

import * as fs from 'fs';
import * as path from 'path';

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .trim();
}

function generateTemplate(templateName: string): void {
  const templateId = slugify(templateName);
  const templateDir = path.join(__dirname, '..', 'templates', 'base_templates', templateId);

  if (fs.existsSync(templateDir)) {
    console.error(`❌ Template already exists: ${templateId}`);
    process.exit(1);
  }

  fs.mkdirSync(templateDir, { recursive: true });

  // Create template config
  const templateConfig = {
    id: templateId,
    name: templateName,
    targetIndustries: [],
    primaryGoal: [],
    defaultPages: ['home'],
    pageToModuleIds: {
      home: ['hero_basic'],
    },
    description: `Template for ${templateName}`,
  };

  fs.writeFileSync(
    path.join(templateDir, 'template.json'),
    JSON.stringify(templateConfig, null, 2)
  );

  // Create README
  const readme = `# ${templateName}

Template description and usage notes.

## Pages

- home

## Modules

- hero_basic

## Usage

This template is designed for...

## Customization

Add notes about how to customize this template.
`;

  fs.writeFileSync(path.join(templateDir, 'README.md'), readme);

  console.log(`✅ Template created: ${templateDir}`);
  console.log(`\nEdit template.json to configure pages and modules.`);
}

const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('Usage: generate-template.ts <template-name>');
  process.exit(1);
}

generateTemplate(args[0]);

