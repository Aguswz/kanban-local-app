#!/usr/bin/env python3
"""
🔗 GitHub Integration
Integración con GitHub Projects y Issues para sincronizar el tablero Kanban
"""

import os
import json
import requests
import datetime
from pathlib import Path

class GitHubIntegration:
    def __init__(self, token=None, repo=None, project_id=None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.repo = repo or os.getenv('GITHUB_REPO')  # formato: "owner/repo"
        self.project_id = project_id or os.getenv('GITHUB_PROJECT_ID')
        
        self.base_path = Path(__file__).parent.parent
        self.config_file = self.base_path / "tools" / "github-config.json"
        
        # Cargar configuración si existe
        self.load_config()
        
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def load_config(self):
        """Cargar configuración de GitHub"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.token = self.token or config.get('token')
                self.repo = self.repo or config.get('repo')
                self.project_id = self.project_id or config.get('project_id')
    
    def save_config(self):
        """Guardar configuración de GitHub"""
        config = {
            'repo': self.repo,
            'project_id': self.project_id,
            'last_sync': datetime.datetime.now().isoformat()
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def setup(self, token, repo, project_id=None):
        """Configurar integración inicial"""
        self.token = token
        self.repo = repo
        self.project_id = project_id
        
        self.headers['Authorization'] = f'token {self.token}'
        
        # Verificar conexión
        if self.test_connection():
            self.save_config()
            print("✅ Integración con GitHub configurada correctamente")
            return True
        else:
            print("❌ Error al configurar integración con GitHub")
            return False
    
    def test_connection(self):
        """Probar conexión con GitHub"""
        if not self.token or not self.repo:
            print("⚠️ Token o repositorio no configurados")
            return False
        
        try:
            url = f"https://api.github.com/repos/{self.repo}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                repo_info = response.json()
                print(f"✅ Conectado a: {repo_info['full_name']}")
                return True
            else:
                print(f"❌ Error de conexión: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def create_issue_from_story(self, story_file):
        """Crear GitHub Issue desde historia de usuario"""
        if not self.token or not self.repo:
            print("⚠️ GitHub no configurado")
            return None
        
        # Leer archivo de historia
        with open(story_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraer información
        title = self.extract_title_from_story(content)
        body = self.format_story_for_github(content)
        labels = self.extract_labels_from_story(content)
        
        # Crear issue
        issue_data = {
            'title': title,
            'body': body,
            'labels': labels
        }
        
        try:
            url = f"https://api.github.com/repos/{self.repo}/issues"
            response = requests.post(url, headers=self.headers, json=issue_data)
            
            if response.status_code == 201:
                issue = response.json()
                print(f"✅ Issue creado: #{issue['number']} - {title}")
                
                # Actualizar archivo local con número de issue
                self.update_story_with_issue_number(story_file, issue['number'])
                
                return issue
            else:
                print(f"❌ Error creando issue: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def extract_title_from_story(self, content):
        """Extraer título de la historia"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('**Como**'):
                # Buscar la línea "Quiero"
                for i, next_line in enumerate(lines):
                    if next_line.startswith('**Quiero**'):
                        return next_line.replace('**Quiero**', '').strip()
        
        # Fallback: usar primera línea que no sea header
        for line in lines:
            if line.strip() and not line.startswith('#'):
                return line.strip()
        
        return "Nueva historia de usuario"
    
    def format_story_for_github(self, content):
        """Formatear historia para GitHub Issue"""
        # Mantener formato markdown pero agregar contexto
        github_body = f"""<!-- Sincronizado desde tablero Kanban local -->

{content}

---
*Esta issue fue creada automáticamente desde el tablero Kanban local*
"""
        return github_body
    
    def extract_labels_from_story(self, content):
        """Extraer labels de la historia"""
        labels = ['user-story']
        
        # Buscar prioridad
        if 'Crítica' in content or 'Crítico' in content:
            labels.append('priority:critical')
        elif 'Alta' in content:
            labels.append('priority:high')
        elif 'Media' in content:
            labels.append('priority:medium')
        elif 'Baja' in content:
            labels.append('priority:low')
        
        # Buscar estimación
        if 'XS' in content:
            labels.append('size:xs')
        elif 'XL' in content:
            labels.append('size:xl')
        elif 'L' in content:
            labels.append('size:l')
        elif 'M' in content:
            labels.append('size:m')
        elif 'S' in content:
            labels.append('size:s')
        
        return labels
    
    def update_story_with_issue_number(self, story_file, issue_number):
        """Actualizar archivo de historia con número de issue"""
        with open(story_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Agregar referencia al issue
        github_section = f"""
## 🔗 GitHub Integration
- **Issue**: #{issue_number}
- **URL**: https://github.com/{self.repo}/issues/{issue_number}
- **Sincronizado**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        
        # Insertar antes de la línea final
        lines = content.split('\n')
        insert_index = -3  # Antes de las últimas líneas de metadata
        
        lines.insert(insert_index, github_section)
        
        with open(story_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def sync_board_to_github(self):
        """Sincronizar tablero completo con GitHub"""
        print("🔄 Iniciando sincronización con GitHub...")
        
        # Buscar archivos de historias y tareas
        stories_dir = self.base_path / "stories"
        tasks_dir = self.base_path / "tasks"
        
        synced_count = 0
        
        # Sincronizar historias
        if stories_dir.exists():
            for story_file in stories_dir.glob("US-*.md"):
                if not self.has_github_issue(story_file):
                    issue = self.create_issue_from_story(story_file)
                    if issue:
                        synced_count += 1
        
        # Sincronizar tareas (como issues con label 'task')
        if tasks_dir.exists():
            for task_file in tasks_dir.glob("T-*.md"):
                if not self.has_github_issue(task_file):
                    issue = self.create_issue_from_task(task_file)
                    if issue:
                        synced_count += 1
        
        print(f"✅ Sincronización completada: {synced_count} items sincronizados")
        return synced_count
    
    def has_github_issue(self, file_path):
        """Verificar si el archivo ya tiene un issue asociado"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return '## 🔗 GitHub Integration' in content or 'Issue**:' in content
    
    def create_issue_from_task(self, task_file):
        """Crear GitHub Issue desde tarea técnica"""
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraer información específica de tarea
        title = self.extract_title_from_task(content)
        body = self.format_task_for_github(content)
        labels = self.extract_labels_from_task(content)
        
        issue_data = {
            'title': title,
            'body': body,
            'labels': labels
        }
        
        try:
            url = f"https://api.github.com/repos/{self.repo}/issues"
            response = requests.post(url, headers=self.headers, json=issue_data)
            
            if response.status_code == 201:
                issue = response.json()
                print(f"✅ Issue de tarea creado: #{issue['number']} - {title}")
                self.update_story_with_issue_number(task_file, issue['number'])
                return issue
            else:
                print(f"❌ Error creando issue de tarea: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def extract_title_from_task(self, content):
        """Extraer título de la tarea"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('**Objetivo**:'):
                return line.replace('**Objetivo**:', '').strip()
        
        return "Nueva tarea técnica"
    
    def format_task_for_github(self, content):
        """Formatear tarea para GitHub Issue"""
        return f"""<!-- Tarea técnica sincronizada desde tablero Kanban local -->

{content}

---
*Esta issue fue creada automáticamente desde el tablero Kanban local*
"""
    
    def extract_labels_from_task(self, content):
        """Extraer labels de la tarea"""
        labels = ['task']
        
        # Buscar tipo de tarea
        if 'Bug' in content:
            labels.append('bug')
        elif 'Mejora' in content:
            labels.append('enhancement')
        elif 'Deuda Técnica' in content:
            labels.append('tech-debt')
        elif 'Investigación' in content:
            labels.append('research')
        
        # Buscar prioridad
        if 'Crítica' in content:
            labels.append('priority:critical')
        elif 'Alta' in content:
            labels.append('priority:high')
        elif 'Media' in content:
            labels.append('priority:medium')
        elif 'Baja' in content:
            labels.append('priority:low')
        
        return labels

def main():
    integration = GitHubIntegration()
    
    if len(os.sys.argv) < 2:
        print("🔗 GitHub Integration - Comandos disponibles:")
        print("  setup <token> <owner/repo> [project_id]")
        print("  test")
        print("  sync")
        print("  create-issue <story_file>")
        return
    
    command = os.sys.argv[1]
    
    if command == "setup":
        if len(os.sys.argv) < 4:
            print("❌ Uso: setup <token> <owner/repo> [project_id]")
            return
        
        token = os.sys.argv[2]
        repo = os.sys.argv[3]
        project_id = os.sys.argv[4] if len(os.sys.argv) > 4 else None
        
        integration.setup(token, repo, project_id)
        
    elif command == "test":
        integration.test_connection()
        
    elif command == "sync":
        integration.sync_board_to_github()
        
    elif command == "create-issue":
        if len(os.sys.argv) < 3:
            print("❌ Uso: create-issue <story_file>")
            return
        
        story_file = Path(os.sys.argv[2])
        if story_file.exists():
            integration.create_issue_from_story(story_file)
        else:
            print(f"❌ Archivo no encontrado: {story_file}")
    
    else:
        print(f"❌ Comando desconocido: {command}")

if __name__ == "__main__":
    main()