import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';

const requiredFiles = [
  '.nojekyll',
  '404.html',
  'index.html',
  'robots.txt',
  'sitemap.xml',
  'assets/css/styles.css',
  'assets/js/main.js',
  'assets/images/favicon.svg',
];

const missingRequiredFiles = requiredFiles.filter((file) => !existsSync(file));

if (missingRequiredFiles.length > 0) {
  throw new Error(`Missing required files:\n${missingRequiredFiles.join('\n')}`);
}

function walk(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = join(directory, entry.name);

    if (entry.name === '.git') return [];
    return entry.isDirectory() ? walk(path) : [path];
  });
}

const localReferencePattern = /(?:href|src)="([^"]+)"/g;
const unresolvedReferences = [];

for (const htmlFile of walk('.').filter((file) => file.endsWith('.html'))) {
  const html = readFileSync(htmlFile, 'utf8');

  for (const match of html.matchAll(localReferencePattern)) {
    let reference = match[1];

    if (/^(?:https?:|mailto:|#)/.test(reference)) continue;

    reference = reference.split(/[?#]/)[0];
    let target = resolve(dirname(htmlFile), reference);

    if (reference.endsWith('/')) target = join(target, 'index.html');
    if (!existsSync(target)) unresolvedReferences.push(`${htmlFile}: ${match[1]}`);
  }
}

if (unresolvedReferences.length > 0) {
  throw new Error(`Unresolved local references:\n${unresolvedReferences.join('\n')}`);
}

const stylesheet = readFileSync('assets/css/styles.css', 'utf8');
const cssImportPattern = /@import url\("([^"]+)"\)/g;
const unresolvedImports = [...stylesheet.matchAll(cssImportPattern)]
  .map((match) => match[1])
  .filter((reference) => !existsSync(join('assets/css', reference)));

if (unresolvedImports.length > 0) {
  throw new Error(`Unresolved CSS imports:\n${unresolvedImports.join('\n')}`);
}

console.log('Static website structure and references are valid.');
