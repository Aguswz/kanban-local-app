# 🤝 Contribuir a Team Manager Desktop

¡Gracias por tu interés en contribuir a Team Manager Desktop! Este proyecto está diseñado para ser una herramienta profesional de gestión de equipos con IA integrada.

## 🚀 Cómo Empezar

### Requisitos de Desarrollo

- **Node.js** 18+ 
- **Python** 3.9+
- **Git**
- **npm** o **yarn**

### Configuración del Entorno

1. **Fork y clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/team-manager-desktop.git
   cd team-manager-desktop
   ```

2. **Instalar dependencias**
   ```bash
   # Dependencias principales
   npm install
   
   # Frontend
   cd frontend && npm install && cd ..
   
   # Backend
   cd backend && pip install -r requirements.txt && cd ..
   ```

3. **Configurar variables de entorno**
   ```bash
   # Opcional: Para funcionalidad completa de IA
   cp .env.example .env
   # Editar .env con tus API keys
   ```

4. **Ejecutar en modo desarrollo**
   ```bash
   npm run dev
   ```

## 🏗️ Arquitectura del Proyecto

```
team-manager-desktop/
├── electron/          # Configuración Electron
├── frontend/          # React + TypeScript
├── backend/           # Python + FastAPI
├── docs/              # Documentación
└── build/             # Scripts de construcción
```

### Tecnologías Principales

- **Frontend**: React, TypeScript, Tailwind CSS, Zustand
- **Backend**: Python, FastAPI, SQLAlchemy, SQLite
- **Desktop**: Electron
- **IA**: OpenAI, Anthropic (opcional)

## 📝 Tipos de Contribuciones

### 🐛 Reportar Bugs

Usa el template de issue para bugs:
- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Screenshots si es relevante
- Información del sistema

### 💡 Sugerir Funcionalidades

Para nuevas funcionalidades:
- Describe el problema que resuelve
- Propón una solución
- Considera el impacto en la UX
- Evalúa la complejidad técnica

### 🔧 Contribuir Código

#### Proceso de Desarrollo

1. **Crear una rama**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   # o
   git checkout -b fix/corregir-bug
   ```

2. **Hacer cambios**
   - Sigue las convenciones de código
   - Añade tests si es necesario
   - Actualiza documentación

3. **Commit con formato convencional**
   ```bash
   git commit -m "feat: añadir análisis de riesgos automático"
   git commit -m "fix: corregir cálculo de utilización"
   git commit -m "docs: actualizar guía de instalación"
   ```

4. **Push y crear PR**
   ```bash
   git push origin feature/nueva-funcionalidad
   ```

#### Convenciones de Código

**Frontend (TypeScript/React)**
```typescript
// Usar interfaces para props
interface ComponentProps {
  title: string
  onAction: () => void
}

// Componentes funcionales con tipos
const Component: React.FC<ComponentProps> = ({ title, onAction }) => {
  return <div>{title}</div>
}

// Hooks personalizados con prefijo 'use'
const useCustomHook = () => {
  // lógica del hook
}
```

**Backend (Python)**
```python
# Seguir PEP 8
# Usar type hints
def analyze_workload(teams: List[Team]) -> WorkloadAnalysis:
    """Analizar carga de trabajo de equipos."""
    pass

# Docstrings para funciones públicas
class AIDirector:
    """Director de IA para análisis organizacional."""
    
    def analyze_global_state(self) -> Dict[str, Any]:
        """Analizar estado global de la organización."""
        pass
```

#### Tests

**Frontend**
```bash
cd frontend
npm test
```

**Backend**
```bash
cd backend
pytest
```

**E2E**
```bash
npm run test:e2e
```

## 🎨 Guías de Diseño

### Principios UX

1. **Claridad > Estética**
   - Información esencial primero
   - Jerarquía visual clara
   - Acciones obvias

2. **Profesional y Funcional**
   - Diseño sobrio
   - Optimizado para uso diario
   - Cero distracciones

3. **Accesibilidad**
   - Contraste adecuado
   - Navegación por teclado
   - Textos descriptivos

### Componentes UI

- Usar Tailwind CSS para estilos
- Componentes reutilizables en `frontend/src/components/common/`
- Iconos de Lucide React
- Paleta de colores consistente

## 🧠 Director IA

### Principios del Director IA

El Director IA debe comportarse como un **director de operaciones senior**:

- **Profesional**: Sin lenguaje de chatbot
- **Contextual**: Analiza la situación completa
- **Accionable**: Recomendaciones específicas
- **Proactivo**: Detecta problemas antes de que escalen

### Añadir Nuevas Capacidades IA

1. **Definir el análisis** en `backend/services/ai_director.py`
2. **Crear prompts** específicos en `backend/prompts/`
3. **Añadir endpoints** en `backend/api/ai.py`
4. **Integrar en frontend** via `frontend/src/services/api.ts`

## 📚 Documentación

### Actualizar Documentación

- **README.md**: Información general
- **docs/ARCHITECTURE.md**: Detalles técnicos
- **docs/GETTING_STARTED.md**: Guía de usuario
- Comentarios en código para lógica compleja

### Escribir Documentación

- Lenguaje claro y directo
- Ejemplos prácticos
- Screenshots cuando sea útil
- Mantener actualizada con cambios

## 🔍 Review Process

### Criterios de Revisión

**Funcionalidad**
- ✅ Funciona según especificación
- ✅ No rompe funcionalidad existente
- ✅ Tests pasan
- ✅ Manejo de errores adecuado

**Código**
- ✅ Sigue convenciones del proyecto
- ✅ Código limpio y legible
- ✅ Documentación adecuada
- ✅ Performance aceptable

**UX**
- ✅ Interfaz intuitiva
- ✅ Consistente con diseño existente
- ✅ Accesible
- ✅ Responsive

### Proceso de Review

1. **Automated checks** deben pasar
2. **Code review** por maintainer
3. **Testing** en diferentes plataformas
4. **Merge** cuando esté aprobado

## 🚀 Release Process

### Versionado

Seguimos [Semantic Versioning](https://semver.org/):
- **MAJOR**: Cambios incompatibles
- **MINOR**: Nueva funcionalidad compatible
- **PATCH**: Bug fixes compatibles

### Proceso de Release

1. **Preparar release**
   - Actualizar CHANGELOG.md
   - Bump version en package.json
   - Tag en git

2. **Build y test**
   - Tests completos
   - Build para todas las plataformas
   - Verificación manual

3. **Publicar**
   - GitHub Release
   - Instaladores en releases
   - Actualizar documentación

## 🤔 ¿Necesitas Ayuda?

- **Issues**: Para bugs y sugerencias
- **Discussions**: Para preguntas generales
- **Discord**: Chat en tiempo real (próximamente)
- **Email**: team@teammanager.com

## 📋 Checklist para Contributors

Antes de enviar tu PR:

- [ ] Código sigue las convenciones del proyecto
- [ ] Tests añadidos/actualizados
- [ ] Documentación actualizada
- [ ] Commit messages siguen formato convencional
- [ ] PR description explica los cambios
- [ ] No hay conflictos con main branch
- [ ] Build local exitoso

¡Gracias por contribuir a Team Manager Desktop! 🎉