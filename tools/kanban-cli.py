#!/usr/bin/env python3
"""
🚀 Kanban CLI Tool
Herramienta de línea de comandos para gestionar el tablero Kanban
"""

import os
import sys
import json
import datetime
from pathlib import Path

class KanbanCLI:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.board_path = self.base_path / "kanban" / "board.md"
        self.templates_path = self.base_path / "templates"
        
    def create_story(self, title, description="", priority="Media"):
        """Crear nueva historia de usuario"""
        story_id = f"US-{datetime.date.today()}-{self.get_next_id('US')}"
        
        template_path = self.templates_path / "user-story.md"
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Reemplazar placeholders
        story_content = template.replace('[tipo de usuario]', 'usuario')
        story_content = story_content.replace('[funcionalidad/objetivo]', title)
        story_content = story_content.replace('[beneficio/valor]', description)
        story_content = story_content.replace('[YYYY-MM-DD]-[###]', story_id)
        story_content = story_content.replace('[Crítica/Alta/Media/Baja]', priority)
        
        # Crear archivo
        story_file = self.base_path / "stories" / f"{story_id}.md"
        story_file.parent.mkdir(exist_ok=True)
        
        with open(story_file, 'w', encoding='utf-8') as f:
            f.write(story_content)
        
        print(f"✅ Historia creada: {story_id}")
        print(f"📁 Archivo: {story_file}")
        
        # Agregar al backlog
        self.add_to_backlog(story_id, title, priority)
        
    def create_task(self, title, task_type="Mejora", priority="Media"):
        """Crear nueva tarea técnica"""
        task_id = f"T-{datetime.date.today()}-{self.get_next_id('T')}"
        
        template_path = self.templates_path / "task.md"
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Reemplazar placeholders
        task_content = template.replace('[Qué se necesita hacer]', title)
        task_content = task_content.replace('[YYYY-MM-DD]-[###]', task_id)
        task_content = task_content.replace('[Bug/Mejora/Deuda Técnica/Investigación/Setup]', task_type)
        task_content = task_content.replace('[Crítica/Alta/Media/Baja]', priority)
        
        # Crear archivo
        task_file = self.base_path / "tasks" / f"{task_id}.md"
        task_file.parent.mkdir(exist_ok=True)
        
        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(task_content)
        
        print(f"✅ Tarea creada: {task_id}")
        print(f"📁 Archivo: {task_file}")
        
        # Agregar al backlog
        self.add_to_backlog(task_id, title, priority)
    
    def get_next_id(self, prefix):
        """Obtener siguiente ID disponible"""
        today = datetime.date.today().strftime("%Y-%m-%d")
        existing_files = []
        
        # Buscar archivos existentes
        for folder in ["stories", "tasks", "epics"]:
            folder_path = self.base_path / folder
            if folder_path.exists():
                existing_files.extend(folder_path.glob(f"{prefix}-{today}-*.md"))
        
        if not existing_files:
            return "001"
        
        # Encontrar el número más alto
        numbers = []
        for file in existing_files:
            try:
                num = int(file.stem.split('-')[-1])
                numbers.append(num)
            except ValueError:
                continue
        
        return f"{max(numbers) + 1:03d}" if numbers else "001"
    
    def add_to_backlog(self, item_id, title, priority):
        """Agregar item al backlog del tablero"""
        if not self.board_path.exists():
            print("⚠️ Tablero no encontrado")
            return
        
        with open(self.board_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determinar sección según prioridad
        if priority in ["Crítica", "Crítico"]:
            section = "### 🔴 CRÍTICO"
        elif priority == "Alta":
            section = "### 🟡 ALTA PRIORIDAD"
        else:
            section = "### 🟢 MEDIA/BAJA PRIORIDAD"
        
        # Agregar item
        new_item = f"- [ ] **[{item_id}]** {title}"
        
        # Insertar en la sección correcta
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip() == section:
                lines.insert(i + 1, new_item)
                break
        
        # Guardar cambios
        with open(self.board_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"📋 Agregado al backlog en sección: {section}")
    
    def move_item(self, item_id, from_column, to_column):
        """Mover item entre columnas"""
        print(f"🔄 Moviendo {item_id} de {from_column} a {to_column}")
        # TODO: Implementar lógica de movimiento
        
    def show_status(self):
        """Mostrar estado actual del tablero"""
        print("📊 ESTADO DEL TABLERO KANBAN")
        print("=" * 40)
        
        # Contar items por columna
        columns = {
            "Backlog": 0,
            "Ready": 0,
            "In Progress": 0,
            "Review": 0,
            "Blocked": 0,
            "Done": 0
        }
        
        if self.board_path.exists():
            with open(self.board_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Contar checkboxes por sección
            lines = content.split('\n')
            current_section = ""
            
            for line in lines:
                if "BACKLOG" in line:
                    current_section = "Backlog"
                elif "READY" in line:
                    current_section = "Ready"
                elif "EN PROGRESO" in line:
                    current_section = "In Progress"
                elif "REVISIÓN" in line:
                    current_section = "Review"
                elif "BLOQUEADO" in line:
                    current_section = "Blocked"
                elif "HECHO" in line:
                    current_section = "Done"
                elif line.strip().startswith("- [ ]") and current_section:
                    columns[current_section] += 1
        
        # Mostrar resumen
        for column, count in columns.items():
            status = "✅" if count <= 3 else "⚠️" if count <= 5 else "🚨"
            print(f"{status} {column}: {count} items")
        
        print(f"\n🎯 WIP Total: {columns['Ready'] + columns['In Progress'] + columns['Review']}")
        print(f"🚫 Bloqueados: {columns['Blocked']}")

def main():
    cli = KanbanCLI()
    
    if len(sys.argv) < 2:
        print("🚀 Kanban CLI - Comandos disponibles:")
        print("  story <título> [descripción] [prioridad]")
        print("  task <título> [tipo] [prioridad]")
        print("  status")
        print("  move <id> <from> <to>")
        return
    
    command = sys.argv[1]
    
    if command == "story":
        title = sys.argv[2] if len(sys.argv) > 2 else "Nueva historia"
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        priority = sys.argv[4] if len(sys.argv) > 4 else "Media"
        cli.create_story(title, description, priority)
        
    elif command == "task":
        title = sys.argv[2] if len(sys.argv) > 2 else "Nueva tarea"
        task_type = sys.argv[3] if len(sys.argv) > 3 else "Mejora"
        priority = sys.argv[4] if len(sys.argv) > 4 else "Media"
        cli.create_task(title, task_type, priority)
        
    elif command == "status":
        cli.show_status()
        
    elif command == "move":
        if len(sys.argv) < 5:
            print("❌ Uso: move <id> <from> <to>")
            return
        item_id = sys.argv[2]
        from_col = sys.argv[3]
        to_col = sys.argv[4]
        cli.move_item(item_id, from_col, to_col)
        
    else:
        print(f"❌ Comando desconocido: {command}")

if __name__ == "__main__":
    main()