// Test script to verify build works
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const scriptPath = join(__dirname, 'scripts', 'build-site-from-config.ts');
const configPath = join(__dirname, 'examples', 'example-builder.json');

console.log('🔨 Starting Forge Site Build Test');
console.log(`Script: ${scriptPath}`);
console.log(`Config: ${configPath}`);

try {
  const result = execSync(`npx tsx "${scriptPath}" "${configPath}"`, {
    encoding: 'utf8',
    cwd: __dirname,
    stdio: 'inherit'
  });
  console.log('\n✅ Build completed successfully');
} catch (error) {
  console.error('\n❌ Build failed:');
  console.error(error.message);
  process.exit(1);
}
