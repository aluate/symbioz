#!/usr/bin/env node
/**
 * Simple test script to verify Forge Site build works
 * This will run the build and check for expected output files
 */

import { execSync } from 'child_process';
import { existsSync, readdirSync, statSync, readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const scriptPath = join(__dirname, 'scripts', 'build-site-from-config.ts');
const configPath = join(__dirname, 'examples', 'example-builder.json');
const outputBase = join(__dirname, 'output');

console.log('🧪 Forge Site Build Test\n');
console.log('─'.repeat(50));

// Step 1: Verify inputs exist
console.log('\n1️⃣ Checking inputs...');
if (!existsSync(configPath)) {
  console.error(`❌ Config file not found: ${configPath}`);
  process.exit(1);
}
console.log(`   ✓ Config file exists: ${configPath}`);

if (!existsSync(scriptPath)) {
  console.error(`❌ Build script not found: ${scriptPath}`);
  process.exit(1);
}
console.log(`   ✓ Build script exists: ${scriptPath}`);

// Step 2: Run the build
console.log('\n2️⃣ Running build script...');
try {
  const output = execSync(`npx tsx "${scriptPath}" "${configPath}"`, {
    encoding: 'utf8',
    cwd: __dirname,
    stdio: 'pipe'
  });
  console.log('   ✓ Build command executed');
  if (output) {
    console.log('   Build output:');
    console.log(output.split('\n').map(line => `   ${line}`).join('\n'));
  }
} catch (error) {
  console.error('   ❌ Build failed:');
  if (error.stdout) console.error(error.stdout);
  if (error.stderr) console.error(error.stderr);
  console.error(error.message);
  process.exit(1);
}

// Step 3: Check for output directory
console.log('\n3️⃣ Checking output directory...');
const outputDirs = readdirSync(outputBase).filter(item => {
  const itemPath = join(outputBase, item);
  return statSync(itemPath).isDirectory() && item !== '.git';
});

if (outputDirs.length === 0) {
  console.error('   ❌ No output directories found');
  process.exit(1);
}

const siteDir = outputDirs[0]; // Should be "acme-builders" or similar
const sitePath = join(outputBase, siteDir);
console.log(`   ✓ Found output directory: ${siteDir}`);

// Step 4: Verify expected files
console.log('\n4️⃣ Verifying generated files...');
const requiredFiles = [
  'app/page.tsx',
  'app/layout.tsx',
  'app/globals.css',
  'components/HeroBasic.tsx',
  'components/ServicesGrid.tsx',
  'components/ProjectGalleryGrid.tsx',
  'components/TestimonialsStrip.tsx',
  'components/ContactFormSimple.tsx',
  'package.json',
  'tsconfig.json',
  'tailwind.config.js',
  'next.config.js'
];

let allFilesExist = true;
for (const file of requiredFiles) {
  const filePath = join(sitePath, file);
  if (existsSync(filePath)) {
    console.log(`   ✓ ${file}`);
  } else {
    console.log(`   ❌ ${file} - MISSING`);
    allFilesExist = false;
  }
}

if (!allFilesExist) {
  console.error('\n❌ Some required files are missing');
  process.exit(1);
}

// Step 5: Check for module imports in page.tsx
console.log('\n5️⃣ Verifying module integration...');
const pageContent = readFileSync(join(sitePath, 'app/page.tsx'), 'utf8');
const moduleNames = ['HeroBasic', 'ServicesGrid', 'ProjectGalleryGrid', 'TestimonialsStrip', 'ContactFormSimple'];
let allModulesFound = true;

for (const moduleName of moduleNames) {
  if (pageContent.includes(moduleName)) {
    console.log(`   ✓ ${moduleName} imported and used`);
  } else {
    console.log(`   ❌ ${moduleName} not found in page.tsx`);
    allModulesFound = false;
  }
}

if (!allModulesFound) {
  console.error('\n❌ Some modules are not integrated');
  process.exit(1);
}

// Step 6: Check package.json
console.log('\n6️⃣ Verifying package.json...');
const packageJson = JSON.parse(readFileSync(join(sitePath, 'package.json'), 'utf8'));
const requiredDeps = ['next', 'react', 'react-dom'];
const requiredDevDeps = ['typescript', 'tailwindcss'];

let depsOk = true;
for (const dep of requiredDeps) {
  if (packageJson.dependencies && packageJson.dependencies[dep]) {
    console.log(`   ✓ ${dep} in dependencies`);
  } else {
    console.log(`   ❌ ${dep} missing from dependencies`);
    depsOk = false;
  }
}

for (const dep of requiredDevDeps) {
  if (packageJson.devDependencies && packageJson.devDependencies[dep]) {
    console.log(`   ✓ ${dep} in devDependencies`);
  } else {
    console.log(`   ❌ ${dep} missing from devDependencies`);
    depsOk = false;
  }
}

if (!depsOk) {
  console.error('\n❌ Package.json missing required dependencies');
  process.exit(1);
}

// Success!
console.log('\n' + '─'.repeat(50));
console.log('✅ BUILD TEST PASSED');
console.log('─'.repeat(50));
console.log(`\n📁 Generated site: ${sitePath}`);
console.log('\n📋 Next steps:');
console.log(`   cd "${sitePath}"`);
console.log('   npm install');
console.log('   npm run dev');
console.log('\n🎉 Forge Site is ready to generate websites!\n');
