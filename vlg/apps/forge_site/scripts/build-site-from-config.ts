#!/usr/bin/env node

/**
 * Forge Site — Build Site From Config
 * 
 * Takes a business.json file and generates a complete Next.js website.
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

// Get __dirname for ES modules (tsx supports this)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

interface BusinessConfig {
  businessName: string;
  industry: string;
  primaryGoal: 'GET_LEADS' | 'SELL_PRODUCTS' | 'CREDIBILITY' | 'CLARITY';
  description?: string;
  serviceAreas?: string[];
  services?: Array<{ name: string; shortDescription?: string; flagship?: boolean }>;
  hasProducts?: boolean;
  products?: Array<{ name: string; price: number; description?: string; images?: string[] }>;
  projects?: Array<{ title: string; location?: string; type?: string; images?: string[]; description?: string }>;
  testimonials?: Array<{ quote: string; name?: string; role?: string; location?: string }>;
  contact?: {
    phone?: string;
    email?: string;
    address?: string;
    preferredContactMethod?: string;
    hours?: string;
  };
  templateId?: string;
  imagesProvided?: boolean;
  // Brand generation fields
  brandTokensPath?: string;
  brandInput?: {
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
  };
}

interface ModuleDefinition {
  id: string;
  name: string;
  category: string;
  intentTags: string[];
  requiredFields: string[];
  optionalFields: string[];
  layoutComponentPath: string;
  recommendedUseCases: string[];
}

interface Template {
  id: string;
  name: string;
  targetIndustries: string[];
  primaryGoal: string[];
  defaultPages: string[];
  pageToModuleIds: Record<string, string[]>;
}

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .trim();
}

function loadJSON<T>(filePath: string): T {
  const content = fs.readFileSync(filePath, 'utf-8');
  return JSON.parse(content);
}

function selectTemplate(business: BusinessConfig, templates: Template[]): Template {
  // Explicit template selection
  if (business.templateId) {
    const explicit = templates.find(t => t.id === business.templateId);
    if (explicit) return explicit;
  }

  // Auto-select based on primaryGoal
  if (business.primaryGoal === 'SELL_PRODUCTS' || business.hasProducts) {
    const commerce = templates.find(t => t.id === 'commerce-lite');
    if (commerce) return commerce;
  }

  if (business.primaryGoal === 'GET_LEADS') {
    const lead = templates.find(t => t.id === 'lead-capture');
    if (lead) return lead;
  }

  // Default to simple-builder-landing
  const defaultTemplate = templates.find(t => t.id === 'simple-builder-landing');
  return defaultTemplate || templates[0];
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

function loadBrandTokens(brandTokensPath: string): BrandTokens | null {
  if (!fs.existsSync(brandTokensPath)) {
    return null;
  }
  try {
    return loadJSON<BrandTokens>(brandTokensPath);
  } catch {
    return null;
  }
}

function generateBrandFromInput(
  business: BusinessConfig,
  outputDir: string
): BrandTokens | null {
  if (!business.brandInput) {
    return null;
  }

  console.log('🎨 Generating brand system from input...');

  // Import brand generation logic (simplified inline version)
  // In production, this would call the separate script or use AI/LLM
  const { execSync } = require('child_process');
  const brandTokensPath = path.join(outputDir, 'brand-tokens.json');
  const tempInputPath = path.join(outputDir, '.brand-input-temp.json');

  try {
    // Write brand input to temp file
    fs.writeFileSync(tempInputPath, JSON.stringify(business.brandInput, null, 2));

    // Run brand generation script
    const scriptPath = path.join(__dirname, 'generate-brand-from-input.ts');
    execSync(
      `npx tsx "${scriptPath}" "${tempInputPath}" "${business.businessName}" "${brandTokensPath}"`,
      { stdio: 'inherit' }
    );

    // Load generated tokens
    if (fs.existsSync(brandTokensPath)) {
      const tokens = loadBrandTokens(brandTokensPath);
      // Clean up temp file
      if (fs.existsSync(tempInputPath)) {
        fs.unlinkSync(tempInputPath);
      }
      return tokens;
    }
  } catch (error) {
    console.warn('⚠️  Brand generation failed, using defaults:', error);
    // Clean up temp file
    if (fs.existsSync(tempInputPath)) {
      fs.unlinkSync(tempInputPath);
    }
  }

  return null;
}

function getBrandTokens(business: BusinessConfig, outputDir: string): BrandTokens | null {
  // Priority 1: Use provided brand tokens path
  if (business.brandTokensPath) {
    console.log(`🎨 Loading brand tokens from: ${business.brandTokensPath}`);
    const tokens = loadBrandTokens(business.brandTokensPath);
    if (tokens) {
      return tokens;
    }
    console.warn('⚠️  Brand tokens file not found, falling back to generation or defaults');
  }

  // Priority 2: Generate from brand input
  if (business.brandInput) {
    const generated = generateBrandFromInput(business, outputDir);
    if (generated) {
      return generated;
    }
  }

  // Priority 3: Return null (will use Forge Site defaults)
  return null;
}

function generateCopy(field: string, context: BusinessConfig): string {
  // Simple copy generation based on field type and context
  // In a real implementation, this would use AI or templates
  
  if (field === 'headline') {
    return `${context.businessName} — ${context.description || 'Professional Services'}`;
  }
  
  if (field === 'subheadline') {
    return context.description || `Quality ${context.industry} services in ${context.serviceAreas?.[0] || 'your area'}`;
  }

  return `Generated content for ${field}`;
}

function buildSite(businessPath: string, outputBase: string = 'output'): void {
  console.log('🔨 Forge Site Builder\n');

  // Load business config
  if (!fs.existsSync(businessPath)) {
    console.error(`❌ Business config not found: ${businessPath}`);
    process.exit(1);
  }

  const business: BusinessConfig = loadJSON<BusinessConfig>(businessPath);
  console.log(`📋 Building site for: ${business.businessName}`);

  // Load registries
  const moduleRegistry: ModuleDefinition[] = loadJSON<ModuleDefinition[]>(
    path.join(__dirname, '../data/module_registry.json')
  );
  const templateIndex = loadJSON<{ templates: Template[] }>(
    path.join(__dirname, '../data/template_index.json')
  );

  // Select template
  const template = selectTemplate(business, templateIndex.templates);
  console.log(`📐 Template: ${template.name} (${template.id})`);

  // Create output directory
  const siteSlug = slugify(business.businessName);
  const outputDir = path.join(__dirname, '..', outputBase, siteSlug);
  
  if (fs.existsSync(outputDir)) {
    console.log(`⚠️  Output directory exists, cleaning: ${outputDir}`);
    fs.rmSync(outputDir, { recursive: true });
  }
  
  fs.mkdirSync(outputDir, { recursive: true });
  console.log(`📁 Output: ${outputDir}`);

  // Load or generate brand tokens
  const brandTokens = getBrandTokens(business, outputDir);
  const usingCustomBrand = brandTokens !== null;
  if (usingCustomBrand) {
    console.log(`🎨 Using custom brand: ${brandTokens.brandName}`);
    console.log(`   Personality: ${brandTokens.personality.join(', ')}`);
    console.log(`   Primary Color: ${brandTokens.colors.primary.name} (${brandTokens.colors.primary.hex})`);
  } else {
    console.log(`🎨 Using default Forge Site brand tokens`);
  }

  // Build pages
  const pages = template.defaultPages;
  const modulesUsed: string[] = [];

  console.log(`\n📄 Building ${pages.length} pages:`);
  pages.forEach(pageName => {
    console.log(`  - ${pageName}`);
    const moduleIds = template.pageToModuleIds[pageName] || [];
    moduleIds.forEach(moduleId => {
      if (!modulesUsed.includes(moduleId)) {
        modulesUsed.push(moduleId);
      }
    });
  });

  // Create Next.js structure
  const appDir = path.join(outputDir, 'app');
  const componentsDir = path.join(outputDir, 'components');
  fs.mkdirSync(appDir, { recursive: true });
  fs.mkdirSync(componentsDir, { recursive: true });

  // Copy module components to generated site
  console.log('\n📦 Copying module components...');
  const modulesSourceDir = path.join(__dirname, '..', 'modules', 'page_modules');
  const modulesToCopy = ['HeroBasic', 'ServicesGrid', 'ProjectGalleryGrid', 'TestimonialsStrip', 'ContactFormSimple'];
  
  modulesToCopy.forEach(moduleName => {
    const sourceFile = path.join(modulesSourceDir, `${moduleName}.tsx`);
    const destFile = path.join(componentsDir, `${moduleName}.tsx`);
    if (fs.existsSync(sourceFile)) {
      fs.copyFileSync(sourceFile, destFile);
      console.log(`  ✓ ${moduleName}.tsx`);
    }
  });

  // Generate layout.tsx with brand-aware typography
  const fontFamily = brandTokens?.typography.fontFamily.primary || 'Inter';
  const fontStack = brandTokens?.typography.fontFamily.stack || ['Inter', 'system-ui', '-apple-system', 'sans-serif'];
  
  // Generate font import (simplified - only handles Inter for now)
  // In production, would handle multiple Google Fonts
  const fontVarName = fontFamily.toLowerCase().replace(/\s+/g, '');
  const fontImport = `import { Inter } from 'next/font/google';\n\nconst ${fontVarName} = Inter({ subsets: ['latin'] });`;

  const layoutContent = `import type { Metadata } from 'next';
${fontImport}
import './globals.css';

export const metadata: Metadata = {
  title: '${business.businessName}',
  description: '${business.description || `${business.businessName} - Professional Services`}',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={${fontVarName}.className}>{children}</body>
    </html>
  );
}
`;

  fs.writeFileSync(path.join(appDir, 'layout.tsx'), layoutContent);

  // Generate globals.css with brand tokens
  const primaryColor = brandTokens?.colors.primary.hex || '#5D7586';
  const secondaryColor = brandTokens?.colors.secondary.hex || '#F4F2EC';
  const backgroundColor = brandTokens?.colors.background.hex || '#F4F2EC';
  const textColor = brandTokens?.colors.text.hex || '#2F3136';
  const accentColor = brandTokens?.colors.accent?.hex || brandTokens?.colors.primary.hex || '#5D7586';

  const globalsCSS = `@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --primary: ${primaryColor};
  --secondary: ${secondaryColor};
  --background: ${backgroundColor};
  --text: ${textColor};
  --accent: ${accentColor};
  ${brandTokens ? `
  /* Brand: ${brandTokens.brandName} */
  /* Personality: ${brandTokens.personality.join(', ')} */
  ` : `
  /* Default Forge Site palette */
  --steel-blue: #5D7586;
  --porcelain: #F4F2EC;
  --graphite: #2F3136;
  --lavender-gray: #D9DCE0;
  `}
}

body {
  background-color: var(--background);
  color: var(--text);
}
`;

  fs.writeFileSync(path.join(appDir, 'globals.css'), globalsCSS);

  // Helper function to get module component name from module ID
  function getModuleComponentName(moduleId: string): string {
    const nameMap: Record<string, string> = {
      'hero_basic': 'HeroBasic',
      'services_grid': 'ServicesGrid',
      'project_gallery_grid': 'ProjectGalleryGrid',
      'testimonial_strip': 'TestimonialsStrip',
      'contact_form_simple': 'ContactFormSimple',
    };
    return nameMap[moduleId] || null;
  }

  // Generate module props as JSX string
  function generateModuleProps(moduleId: string, business: BusinessConfig): string {
    if (moduleId === 'hero_basic') {
      const headline = generateCopy('headline', business);
      const subheadline = generateCopy('subheadline', business);
      return `headline="${headline}" subheadline="${subheadline}" primaryCTA={${JSON.stringify({ label: 'Get in touch', href: '/contact' })}}`;
    } else if (moduleId === 'services_grid') {
      const services = business.services || [];
      return `services={${JSON.stringify(services)}}`;
    } else if (moduleId === 'project_gallery_grid') {
      const projects = business.projects || [];
      return `projects={${JSON.stringify(projects)}}`;
    } else if (moduleId === 'testimonial_strip') {
      const testimonials = business.testimonials || [];
      return `testimonials={${JSON.stringify(testimonials)}}`;
    } else if (moduleId === 'contact_form_simple') {
      const contact = business.contact || {};
      return `contact={${JSON.stringify(contact)}}`;
    }
    return '';
  }

  // Generate page with modules
  function generatePageWithModules(pageName: string, moduleIds: string[]): string {
    const imports: string[] = [];
    const components: string[] = [];

    moduleIds.forEach(moduleId => {
      const componentName = getModuleComponentName(moduleId);
      if (componentName) {
        imports.push(`import ${componentName} from '@/components/${componentName}';`);
        const props = generateModuleProps(moduleId, business);
        components.push(`      <${componentName} ${props} />`);
      }
    });

    if (components.length === 0) {
      return `export default function ${pageName.charAt(0).toUpperCase() + pageName.slice(1)}() {
  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-4">${pageName.charAt(0).toUpperCase() + pageName.slice(1)}</h1>
        <p className="text-lg">Content for ${pageName} page.</p>
      </div>
    </main>
  );
}
`;
    }

    return `import React from 'react';
${imports.join('\n')}

export default function ${pageName.charAt(0).toUpperCase() + pageName.slice(1)}() {
  return (
    <main>
${components.join('\n')}
    </main>
  );
}
`;
  }

  // Generate home page with modules
  const homeModules = template.pageToModuleIds['home'] || [];
  const homePageContent = generatePageWithModules('home', homeModules);
  fs.writeFileSync(path.join(appDir, 'page.tsx'), homePageContent);

  // Generate additional pages with modules
  pages.filter(p => p !== 'home').forEach(pageName => {
    const pageDir = path.join(appDir, pageName);
    fs.mkdirSync(pageDir, { recursive: true });
    
    const pageModules = template.pageToModuleIds[pageName] || [];
    const pageContent = generatePageWithModules(pageName, pageModules);
    
    fs.writeFileSync(path.join(pageDir, 'page.tsx'), pageContent);
  });

  // Generate package.json
  const packageJson = {
    name: siteSlug,
    version: '0.1.0',
    private: true,
    scripts: {
      dev: 'next dev',
      build: 'next build',
      start: 'next start',
      lint: 'next lint',
    },
    dependencies: {
      react: '^18.2.0',
      'react-dom': '^18.2.0',
      next: '^14.0.0',
    },
    devDependencies: {
      typescript: '^5.0.0',
      '@types/node': '^20.0.0',
      '@types/react': '^18.2.0',
      '@types/react-dom': '^18.2.0',
      tailwindcss: '^3.3.0',
      postcss: '^8.4.0',
      autoprefixer: '^10.4.0',
    },
  };

  fs.writeFileSync(
    path.join(outputDir, 'package.json'),
    JSON.stringify(packageJson, null, 2)
  );

  // Generate tsconfig.json
  const tsconfig = {
    compilerOptions: {
      target: 'ES2017',
      lib: ['dom', 'dom.iterable', 'esnext'],
      allowJs: true,
      skipLibCheck: true,
      strict: true,
      noEmit: true,
      esModuleInterop: true,
      module: 'esnext',
      moduleResolution: 'bundler',
      resolveJsonModule: true,
      isolatedModules: true,
      jsx: 'preserve',
      incremental: true,
      plugins: [{ name: 'next' }],
      paths: {
        '@/*': ['./*'],
      },
      baseUrl: '.',
    },
    include: ['next-env.d.ts', '**/*.ts', '**/*.tsx', '.next/types/**/*.ts'],
    exclude: ['node_modules'],
  };

  fs.writeFileSync(
    path.join(outputDir, 'tsconfig.json'),
    JSON.stringify(tsconfig, null, 2)
  );

  // Generate next.config.js
  const nextConfig = `/** @type {import('next').NextConfig} */
const nextConfig = {};

module.exports = nextConfig;
`;

  fs.writeFileSync(path.join(outputDir, 'next.config.js'), nextConfig);

  // Generate tailwind.config.js with brand colors
  const tailwindConfig = `/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'primary': '${primaryColor}',
        'secondary': '${secondaryColor}',
        'background': '${backgroundColor}',
        'text': '${textColor}',
        'accent': '${accentColor}',
        ${!brandTokens ? `
        'steel-blue': '#5D7586',
        'porcelain': '#F4F2EC',
        'graphite': '#2F3136',
        'lavender-gray': '#D9DCE0',
        ` : ''}
      },
      fontFamily: {
        sans: ${JSON.stringify(brandTokens?.typography.fontFamily.stack || ['Inter', 'system-ui', '-apple-system', 'sans-serif'])},
      },
    },
  },
  plugins: [],
};
`;

  fs.writeFileSync(path.join(outputDir, 'tailwind.config.js'), tailwindConfig);

  // Generate postcss.config.js
  const postcssConfig = `module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
`;

  fs.writeFileSync(path.join(outputDir, 'postcss.config.js'), postcssConfig);

  // Generate .gitignore
  const gitignore = `# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env files
.env*.local

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts
`;

  fs.writeFileSync(path.join(outputDir, '.gitignore'), gitignore);

  // Build report
  console.log(`\n✅ Build Complete\n`);
  console.log(`Build Report: ${business.businessName}`);
  console.log('─'.repeat(40));
  console.log(`Template: ${template.name}`);
  console.log(`Pages Created: ${pages.length}`);
  pages.forEach(p => console.log(`  - ${p}`));
  console.log(`\nModules Used: ${modulesUsed.length}`);
  modulesUsed.forEach(m => console.log(`  - ${m}`));
  if (usingCustomBrand && brandTokens) {
    console.log(`\nBrand System:`);
    console.log(`  Personality: ${brandTokens.personality.join(', ')}`);
    console.log(`  Primary Color: ${brandTokens.colors.primary.name} (${brandTokens.colors.primary.hex})`);
    console.log(`  Typography: ${brandTokens.typography.fontFamily.primary}`);
  } else {
    console.log(`\nBrand: Using default Forge Site tokens`);
  }
  console.log(`\nOutput: ${outputDir}`);
  console.log(`\nStatus: ✓ Ready for dev server`);
  console.log(`\nTo run:`);
  console.log(`  cd ${outputDir}`);
  console.log(`  npm install`);
  console.log(`  npm run dev`);
}

// CLI entry point
const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('Usage: build-site-from-config.ts <business.json>');
  process.exit(1);
}

const businessPath = path.resolve(args[0]);
buildSite(businessPath);

