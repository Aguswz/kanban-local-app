#!/usr/bin/env node
/**
 * 🏗️ Script de construcción para Team Manager Desktop
 * Automatiza la construcción completa de la aplicación
 */

const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

const ROOT_DIR = path.join(__dirname, '..')
const FRONTEND_DIR = path.join(ROOT_DIR, 'frontend')
const BACKEND_DIR = path.join(ROOT_DIR, 'backend')
const DIST_DIR = path.join(ROOT_DIR, 'dist')

console.log('🚀 Iniciando construcción de Team Manager Desktop...\n')

// Función para ejecutar comandos
function runCommand(command, cwd = ROOT_DIR) {
  console.log(`📦 Ejecutando: ${command}`)
  console.log(`📁 En directorio: ${cwd}\n`)
  
  try {
    execSync(command, { 
      cwd, 
      stdio: 'inherit',
      env: { ...process.env, NODE_ENV: 'production' }
    })
    console.log('✅ Comando completado exitosamente\n')
  } catch (error) {
    console.error(`❌ Error ejecutando comando: ${command}`)
    console.error(error.message)
    process.exit(1)
  }
}

// Función para verificar dependencias
function checkDependencies() {
  console.log('🔍 Verificando dependencias...\n')
  
  // Verificar Node.js
  try {
    const nodeVersion = execSync('node --version', { encoding: 'utf8' }).trim()
    console.log(`✅ Node.js: ${nodeVersion}`)
  } catch (error) {
    console.error('❌ Node.js no encontrado')
    process.exit(1)
  }
  
  // Verificar Python
  try {
    const pythonVersion = execSync('python --version', { encoding: 'utf8' }).trim()
    console.log(`✅ Python: ${pythonVersion}`)
  } catch (error) {
    console.error('❌ Python no encontrado')
    process.exit(1)
  }
  
  console.log('')
}

// Función para limpiar directorios
function cleanDist() {
  console.log('🧹 Limpiando directorios de construcción...\n')
  
  if (fs.existsSync(DIST_DIR)) {
    fs.rmSync(DIST_DIR, { recursive: true, force: true })
  }
  
  const frontendBuild = path.join(FRONTEND_DIR, 'build')
  if (fs.existsSync(frontendBuild)) {
    fs.rmSync(frontendBuild, { recursive: true, force: true })
  }
  
  const backendDist = path.join(BACKEND_DIR, 'dist')
  if (fs.existsSync(backendDist)) {
    fs.rmSync(backendDist, { recursive: true, force: true })
  }
  
  console.log('✅ Directorios limpiados\n')
}

// Función para instalar dependencias
function installDependencies() {
  console.log('📦 Instalando dependencias...\n')
  
  // Dependencias del proyecto principal
  if (fs.existsSync(path.join(ROOT_DIR, 'package.json'))) {
    runCommand('npm install', ROOT_DIR)
  }
  
  // Dependencias del frontend
  if (fs.existsSync(path.join(FRONTEND_DIR, 'package.json'))) {
    runCommand('npm install', FRONTEND_DIR)
  }
  
  // Dependencias del backend
  if (fs.existsSync(path.join(BACKEND_DIR, 'requirements.txt'))) {
    runCommand('pip install -r requirements.txt', BACKEND_DIR)
  }
}

// Función para construir frontend
function buildFrontend() {
  console.log('🎨 Construyendo frontend...\n')
  
  if (!fs.existsSync(path.join(FRONTEND_DIR, 'package.json'))) {
    console.log('⚠️ Frontend no encontrado, saltando...\n')
    return
  }
  
  runCommand('npm run build', FRONTEND_DIR)
  
  // Verificar que se generó el build
  const buildDir = path.join(FRONTEND_DIR, 'build')
  if (!fs.existsSync(buildDir)) {
    console.error('❌ Build del frontend no se generó correctamente')
    process.exit(1)
  }
  
  console.log('✅ Frontend construido exitosamente\n')
}

// Función para construir backend
function buildBackend() {
  console.log('⚙️ Construyendo backend...\n')
  
  if (!fs.existsSync(path.join(BACKEND_DIR, 'main.py'))) {
    console.log('⚠️ Backend no encontrado, saltando...\n')
    return
  }
  
  // Crear ejecutable con PyInstaller
  const pyinstallerCommand = [
    'python -m PyInstaller',
    '--onefile',
    '--name team-manager-backend',
    '--distpath dist',
    '--workpath build',
    '--specpath build',
    'main.py'
  ].join(' ')
  
  runCommand(pyinstallerCommand, BACKEND_DIR)
  
  // Verificar que se generó el ejecutable
  const executableName = process.platform === 'win32' ? 'team-manager-backend.exe' : 'team-manager-backend'
  const executablePath = path.join(BACKEND_DIR, 'dist', executableName)
  
  if (!fs.existsSync(executablePath)) {
    console.error('❌ Ejecutable del backend no se generó correctamente')
    process.exit(1)
  }
  
  console.log('✅ Backend construido exitosamente\n')
}

// Función para empaquetar aplicación Electron
function packageElectron() {
  console.log('📱 Empaquetando aplicación Electron...\n')
  
  // Determinar plataforma
  const platform = process.platform
  let packageCommand = 'npm run package'
  
  if (process.argv.includes('--win')) {
    packageCommand = 'npm run package:win'
  } else if (process.argv.includes('--mac')) {
    packageCommand = 'npm run package:mac'
  } else if (process.argv.includes('--linux')) {
    packageCommand = 'npm run package:linux'
  }
  
  runCommand(packageCommand, ROOT_DIR)
  
  console.log('✅ Aplicación empaquetada exitosamente\n')
}

// Función para mostrar resumen
function showSummary() {
  console.log('🎉 ¡Construcción completada exitosamente!\n')
  
  console.log('📁 Archivos generados:')
  
  if (fs.existsSync(DIST_DIR)) {
    const distFiles = fs.readdirSync(DIST_DIR)
    distFiles.forEach(file => {
      const filePath = path.join(DIST_DIR, file)
      const stats = fs.statSync(filePath)
      const size = (stats.size / 1024 / 1024).toFixed(2)
      console.log(`   📦 ${file} (${size} MB)`)
    })
  }
  
  console.log('\n🚀 La aplicación está lista para distribuir!')
  console.log('📍 Ubicación:', DIST_DIR)
}

// Función principal
async function main() {
  try {
    const startTime = Date.now()
    
    // Verificar argumentos
    const args = process.argv.slice(2)
    const skipDeps = args.includes('--skip-deps')
    const skipClean = args.includes('--skip-clean')
    
    // Ejecutar pasos de construcción
    checkDependencies()
    
    if (!skipClean) {
      cleanDist()
    }
    
    if (!skipDeps) {
      installDependencies()
    }
    
    buildFrontend()
    buildBackend()
    packageElectron()
    
    const endTime = Date.now()
    const duration = ((endTime - startTime) / 1000).toFixed(2)
    
    showSummary()
    console.log(`\n⏱️ Tiempo total: ${duration} segundos`)
    
  } catch (error) {
    console.error('\n❌ Error durante la construcción:')
    console.error(error.message)
    process.exit(1)
  }
}

// Ejecutar si es llamado directamente
if (require.main === module) {
  main()
}

module.exports = {
  buildFrontend,
  buildBackend,
  packageElectron
}