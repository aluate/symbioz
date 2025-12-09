// Wrapper to run the build script
const { execSync } = require('child_process');
const path = require('path');

const scriptPath = path.join(__dirname, 'scripts', 'build-site-from-config.ts');
const configPath = path.join(__dirname, 'examples', 'example-builder.json');

try {
  console.log('Running build script...');
  const result = execSync(`npx tsx "${scriptPath}" "${configPath}"`, {
    encoding: 'utf8',
    cwd: __dirname,
    stdio: 'inherit'
  });
  console.log(result);
} catch (error) {
  console.error('Build failed:');
  console.error(error.message);
  if (error.stdout) console.error('STDOUT:', error.stdout);
  if (error.stderr) console.error('STDERR:', error.stderr);
  process.exit(1);
}

