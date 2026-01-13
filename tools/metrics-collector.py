#!/usr/bin/env python3
"""
📊 Metrics Collector
Recolector automático de métricas ágiles para el tablero Kanban
"""

import os
import json
import datetime
import re
from pathlib import Path
from collections import defaultdict

class MetricsCollector:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.board_path = self.base_path / "kanban" / "board.md"
        self.metrics_path = self.base_path / "metrics"
        self.data_file = self.metrics_path / "data.json"
        
        # Crear directorio de métricas si no existe
        self.metrics_path.mkdir(exist_ok=True)
        
        # Cargar datos históricos
        self.load_historical_data()
    
    def load_historical_data(self):
        """Cargar datos históricos de métricas"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "daily_snapshots": [],
                "item_history": {},
                "metrics_history": []
            }
    
    def save_data(self):
        """Guardar datos de métricas"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def take_daily_snapshot(self):
        """Tomar snapshot diario del tablero"""
        if not self.board_path.exists():
            print("⚠️ Tablero no encontrado")
            return
        
        with open(self.board_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Analizar contenido del tablero
        snapshot = {
            "date": datetime.date.today().isoformat(),
            "timestamp": datetime.datetime.now().isoformat(),
            "columns": self.analyze_board_content(content),
            "wip_limits": self.extract_wip_limits(content),
            "blocked_items": self.count_blocked_items(content)
        }
        
        # Agregar a historial
        self.data["daily_snapshots"].append(snapshot)
        
        # Mantener solo últimos 90 días
        cutoff_date = datetime.date.today() - datetime.timedelta(days=90)
        self.data["daily_snapshots"] = [
            s for s in self.data["daily_snapshots"] 
            if datetime.date.fromisoformat(s["date"]) >= cutoff_date
        ]
        
        self.save_data()
        print(f"📸 Snapshot guardado para {snapshot['date']}")
        
        return snapshot
    
    def analyze_board_content(self, content):
        """Analizar contenido del tablero por columnas"""
        columns = {
            "backlog": [],
            "ready": [],
            "in_progress": [],
            "review": [],
            "blocked": [],
            "done": []
        }
        
        lines = content.split('\n')
        current_column = None
        
        for line in lines:
            line = line.strip()
            
            # Identificar columnas
            if "BACKLOG" in line.upper():
                current_column = "backlog"
            elif "READY" in line.upper() or "REFINADO" in line.upper():
                current_column = "ready"
            elif "EN PROGRESO" in line.upper() or "IN PROGRESS" in line.upper():
                current_column = "in_progress"
            elif "REVISIÓN" in line.upper() or "REVIEW" in line.upper():
                current_column = "review"
            elif "BLOQUEADO" in line.upper() or "BLOCKED" in line.upper():
                current_column = "blocked"
            elif "HECHO" in line.upper() or "DONE" in line.upper():
                current_column = "done"
            
            # Extraer items
            if current_column and line.startswith("- [ ]"):
                item = self.extract_item_info(line)
                if item:
                    columns[current_column].append(item)
        
        return columns
    
    def extract_item_info(self, line):
        """Extraer información de un item del tablero"""
        # Buscar patrón [ID] Título
        match = re.search(r'\*\*\[([^\]]+)\]\*\*\s*(.+)', line)
        if match:
            return {
                "id": match.group(1),
                "title": match.group(2).strip(),
                "type": self.determine_item_type(match.group(1))
            }
        return None
    
    def determine_item_type(self, item_id):
        """Determinar tipo de item basado en ID"""
        if item_id.startswith("US-"):
            return "user_story"
        elif item_id.startswith("T-"):
            return "task"
        elif item_id.startswith("EP-"):
            return "epic"
        else:
            return "unknown"
    
    def extract_wip_limits(self, content):
        """Extraer límites WIP del tablero"""
        wip_limits = {}
        
        # Buscar patrones como "WIP: 0/3"
        matches = re.findall(r'WIP:\s*(\d+)/(\d+)', content)
        
        if matches:
            # Asumir orden: ready, in_progress, review
            columns = ["ready", "in_progress", "review"]
            for i, (current, limit) in enumerate(matches):
                if i < len(columns):
                    wip_limits[columns[i]] = {
                        "current": int(current),
                        "limit": int(limit)
                    }
        
        return wip_limits
    
    def count_blocked_items(self, content):
        """Contar items bloqueados"""
        blocked_section = False
        blocked_count = 0
        
        for line in content.split('\n'):
            if "BLOQUEADO" in line.upper() or "BLOCKED" in line.upper():
                blocked_section = True
            elif line.startswith("##") and blocked_section:
                break
            elif blocked_section and line.strip().startswith("- [ ]"):
                blocked_count += 1
        
        return blocked_count
    
    def calculate_metrics(self):
        """Calcular métricas ágiles"""
        if len(self.data["daily_snapshots"]) < 2:
            print("⚠️ Necesitamos al menos 2 snapshots para calcular métricas")
            return None
        
        # Obtener snapshots recientes
        recent_snapshots = self.data["daily_snapshots"][-14:]  # Últimas 2 semanas
        
        metrics = {
            "date": datetime.date.today().isoformat(),
            "throughput": self.calculate_throughput(recent_snapshots),
            "wip_utilization": self.calculate_wip_utilization(recent_snapshots[-1]),
            "blocked_ratio": self.calculate_blocked_ratio(recent_snapshots[-1]),
            "flow_efficiency": self.calculate_flow_efficiency(recent_snapshots),
            "trend_analysis": self.analyze_trends(recent_snapshots)
        }
        
        # Guardar métricas
        self.data["metrics_history"].append(metrics)
        self.save_data()
        
        return metrics
    
    def calculate_throughput(self, snapshots):
        """Calcular throughput (items completados por período)"""
        if len(snapshots) < 2:
            return 0
        
        # Comparar primer y último snapshot
        first_done = len(snapshots[0]["columns"]["done"])
        last_done = len(snapshots[-1]["columns"]["done"])
        
        days = len(snapshots) - 1
        throughput_per_day = (last_done - first_done) / days if days > 0 else 0
        
        return {
            "items_per_day": round(throughput_per_day, 2),
            "items_per_week": round(throughput_per_day * 7, 2),
            "total_completed": last_done - first_done
        }
    
    def calculate_wip_utilization(self, snapshot):
        """Calcular utilización de límites WIP"""
        wip_limits = snapshot.get("wip_limits", {})
        utilization = {}
        
        for column, limits in wip_limits.items():
            if limits["limit"] > 0:
                utilization[column] = {
                    "percentage": round((limits["current"] / limits["limit"]) * 100, 1),
                    "current": limits["current"],
                    "limit": limits["limit"]
                }
        
        return utilization
    
    def calculate_blocked_ratio(self, snapshot):
        """Calcular ratio de items bloqueados"""
        total_active = 0
        blocked = snapshot["blocked_items"]
        
        # Contar items activos (no en backlog ni done)
        for column in ["ready", "in_progress", "review", "blocked"]:
            total_active += len(snapshot["columns"].get(column, []))
        
        if total_active == 0:
            return 0
        
        return round((blocked / total_active) * 100, 1)
    
    def calculate_flow_efficiency(self, snapshots):
        """Calcular eficiencia de flujo"""
        # Simplificado: ratio de items en progreso vs items esperando
        if not snapshots:
            return 0
        
        latest = snapshots[-1]
        in_progress = len(latest["columns"]["in_progress"])
        waiting = len(latest["columns"]["ready"]) + len(latest["columns"]["review"])
        
        total_active = in_progress + waiting
        if total_active == 0:
            return 0
        
        return round((in_progress / total_active) * 100, 1)
    
    def analyze_trends(self, snapshots):
        """Analizar tendencias en las métricas"""
        if len(snapshots) < 7:
            return {"status": "insufficient_data"}
        
        # Analizar últimos 7 días
        recent = snapshots[-7:]
        
        # Tendencia de throughput
        throughput_trend = []
        for i in range(1, len(recent)):
            prev_done = len(recent[i-1]["columns"]["done"])
            curr_done = len(recent[i]["columns"]["done"])
            throughput_trend.append(curr_done - prev_done)
        
        avg_throughput = sum(throughput_trend) / len(throughput_trend) if throughput_trend else 0
        
        # Tendencia de WIP
        wip_trend = []
        for snapshot in recent:
            total_wip = sum(len(snapshot["columns"][col]) for col in ["ready", "in_progress", "review"])
            wip_trend.append(total_wip)
        
        return {
            "throughput_trend": "increasing" if avg_throughput > 0 else "decreasing" if avg_throughput < 0 else "stable",
            "wip_trend": "increasing" if wip_trend[-1] > wip_trend[0] else "decreasing" if wip_trend[-1] < wip_trend[0] else "stable",
            "avg_daily_throughput": round(avg_throughput, 2),
            "current_wip": wip_trend[-1] if wip_trend else 0
        }
    
    def generate_report(self):
        """Generar reporte de métricas"""
        snapshot = self.take_daily_snapshot()
        metrics = self.calculate_metrics()
        
        if not metrics:
            print("⚠️ No hay suficientes datos para generar reporte completo")
            return
        
        report = f"""# 📊 REPORTE DE MÉTRICAS ÁGILES
*Generado: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*

## 🎯 MÉTRICAS ACTUALES

### Throughput
- **Items por día**: {metrics['throughput']['items_per_day']}
- **Items por semana**: {metrics['throughput']['items_per_week']}
- **Total completado**: {metrics['throughput']['total_completed']}

### Utilización WIP
"""
        
        for column, util in metrics['wip_utilization'].items():
            status = "🔴" if util['percentage'] > 90 else "🟡" if util['percentage'] > 70 else "🟢"
            report += f"- **{column.title()}**: {util['current']}/{util['limit']} ({util['percentage']}%) {status}\n"
        
        report += f"""
### Estado del Flujo
- **Items bloqueados**: {metrics['blocked_ratio']}%
- **Eficiencia de flujo**: {metrics['flow_efficiency']}%

## 📈 TENDENCIAS
- **Throughput**: {metrics['trend_analysis']['throughput_trend']}
- **WIP**: {metrics['trend_analysis']['wip_trend']}
- **WIP actual**: {metrics['trend_analysis']['current_wip']} items

## 🚨 ALERTAS
"""
        
        # Generar alertas
        alerts = []
        if metrics['blocked_ratio'] > 20:
            alerts.append("🔴 Alto porcentaje de items bloqueados")
        if metrics['flow_efficiency'] < 30:
            alerts.append("🟡 Baja eficiencia de flujo")
        
        for util in metrics['wip_utilization'].values():
            if util['percentage'] > 90:
                alerts.append("🔴 Límite WIP cerca del máximo")
        
        if not alerts:
            alerts.append("✅ No hay alertas críticas")
        
        for alert in alerts:
            report += f"- {alert}\n"
        
        # Guardar reporte
        report_file = self.metrics_path / f"report-{datetime.date.today()}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📋 Reporte generado: {report_file}")
        print("\n" + "="*50)
        print(report)

def main():
    collector = MetricsCollector()
    
    if len(os.sys.argv) > 1:
        command = os.sys.argv[1]
        
        if command == "snapshot":
            collector.take_daily_snapshot()
        elif command == "metrics":
            collector.calculate_metrics()
        elif command == "report":
            collector.generate_report()
        else:
            print(f"❌ Comando desconocido: {command}")
    else:
        print("📊 Metrics Collector - Comandos disponibles:")
        print("  snapshot  - Tomar snapshot del tablero")
        print("  metrics   - Calcular métricas")
        print("  report    - Generar reporte completo")

if __name__ == "__main__":
    main()