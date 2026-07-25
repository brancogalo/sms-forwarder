"""
PC App - SMS Forwarder Monitor
Monitora SMS em tempo real via WebSocket
Roda em Windows CMD
"""

import socketio
import sys
import os
from datetime import datetime
from colorama import Fore, Back, Style, init
from collections import deque
import threading
import json

# Inicializar colorama para Windows
init(autoreset=True)

class SMSMonitor:
    def __init__(self, servidor='http://localhost:5000'):
        self.servidor = servidor
        self.sio = socketio.Client()
        self.conectado = False
        self.numeros_ativos = {}
        self.sms_buffer = deque(maxlen=20)  # Últimos 20 SMS
        self.lock = threading.Lock()
        
        # Configurar eventos WebSocket
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('dados_iniciais', self.on_dados_iniciais)
        self.sio.on('novo_sms', self.on_novo_sms)
        self.sio.on('cliente_conectado', self.on_cliente_conectado)
        self.sio.on('cliente_desconectado', self.on_cliente_desconectado)
        self.sio.on('sms_expirados', self.on_sms_expirados)
        self.sio.on('pong', self.on_pong)
    
    def on_connect(self):
        """Conectado ao servidor"""
        self.conectado = True
        self.print_status(f"✅ Conectado ao Backend!", Fore.GREEN)
    
    def on_disconnect(self):
        """Desconectado do servidor"""
        self.conectado = False
        self.print_status("❌ Desconectado do Backend", Fore.RED)
    
    def on_dados_iniciais(self, data):
        """Recebe dados iniciais"""
        with self.lock:
            self.numeros_ativos = {n['numero']: n for n in data.get('numeros', [])}
            
            for sms in data.get('sms', []):
                self.sms_buffer.append(sms)
        
        self.print_status(f"📊 {len(self.numeros_ativos)} números ativos", Fore.CYAN)
        self.limpar_tela()
        self.mostrar_monitor()
    
    def on_novo_sms(self, data):
        """Novo SMS chegou"""
        with self.lock:
            # Adicionar ao buffer
            self.sms_buffer.append(data)
            
            # Atualizar número ativo
            numero = data['numero']
            if numero in self.numeros_ativos:
                self.numeros_ativos[numero]['quantidade'] += 1
                self.numeros_ativos[numero]['ultimo_sms'] = data['timestamp']
            else:
                self.numeros_ativos[numero] = {
                    'numero': numero,
                    'quantidade': 1,
                    'ultimo_sms': data['timestamp'],
                    'status': 'ativo'
                }
        
        # Notificação
        self.print_sms_notificacao(data)
        self.limpar_tela()
        self.mostrar_monitor()
    
    def on_cliente_conectado(self, data):
        """Outro cliente conectado"""
        total = data.get('total_clientes', 0)
        self.print_status(f"👥 {total} clientes conectados", Fore.BLUE)
    
    def on_cliente_desconectado(self, data):
        """Outro cliente desconectado"""
        total = data.get('total_clientes', 0)
        self.print_status(f"👥 {total} clientes conectados", Fore.BLUE)
    
    def on_sms_expirados(self, data):
        """SMS expirados (5 horas) foram deletados"""
        quantidade = data.get('quantidade', 0)
        self.print_status(f"🗑️  {quantidade} SMS expirados removidos", Fore.YELLOW)
    
    def on_pong(self, data):
        """Resposta de ping"""
        pass  # Keep-alive OK
    
    def conectar(self):
        """Conectar ao servidor"""
        try:
            self.print_status(f"🔌 Conectando a {self.servidor}...", Fore.YELLOW)
            self.sio.connect(self.servidor)
            
            # Enviar ping a cada 30 segundos
            threading.Thread(target=self.keep_alive, daemon=True).start()
            
        except Exception as e:
            self.print_status(f"❌ Erro ao conectar: {str(e)}", Fore.RED)
            return False
        
        return True
    
    def keep_alive(self):
        """Keep-alive - envia ping periodicamente"""
        while self.conectado:
            try:
                threading.Event().wait(30)
                if self.conectado:
                    self.sio.emit('ping')
            except:
                break
    
    def limpar_tela(self):
        """Limpar tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_status(self, mensagem, cor=Fore.WHITE):
        """Imprimir mensagem de status"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{cor}[{timestamp}] {mensagem}{Style.RESET_ALL}")
    
    def print_sms_notificacao(self, sms):
        """Notificação de novo SMS"""
        print("\n")
        print(f"{Fore.GREEN}{'='*50}")
        print(f"{Fore.GREEN}📬 NOVO SMS!")
        print(f"{Fore.GREEN}{'='*50}")
        print(f"{Fore.YELLOW}De: {sms['numero']}")
        print(f"{Fore.WHITE}Mensagem: {sms['mensagem'][:100]}")
        print(f"{Fore.CYAN}Hora: {sms['timestamp']}")
        print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}\n")
    
    def mostrar_monitor(self):
        """Mostrar tela do monitor"""
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}  SMS FORWARDER - MONITOR{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
        
        # Status de conexão
        if self.conectado:
            status_str = f"{Fore.GREEN}✓ ONLINE{Style.RESET_ALL}"
        else:
            status_str = f"{Fore.RED}✗ OFFLINE{Style.RESET_ALL}"
        
        print(f"Status: {status_str}")
        print(f"Horário: {datetime.now().strftime('%H:%M:%S')}")
        print(f"\n")
        
        # Números ativos
        print(f"{Fore.YELLOW}NÚMEROS ATIVOS ({len(self.numeros_ativos)}){Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*50}{Style.RESET_ALL}")
        
        if not self.numeros_ativos:
            print(f"{Fore.WHITE}Nenhum número ativo ainda...{Style.RESET_ALL}")
        else:
            for numero, info in sorted(
                self.numeros_ativos.items(),
                key=lambda x: x[1]['ultimo_sms'],
                reverse=True
            ):
                # Status (verde se ativo)
                status_icon = f"{Fore.GREEN}🟢{Style.RESET_ALL}"
                qtd = info['quantidade']
                print(f"{status_icon} {Fore.WHITE}{numero:<20} {Fore.CYAN}({qtd} SMS){Style.RESET_ALL}")
        
        print(f"\n")
        
        # SMS recentes
        print(f"{Fore.YELLOW}ÚLTIMOS SMS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*50}{Style.RESET_ALL}")
        
        if not self.sms_buffer:
            print(f"{Fore.WHITE}Aguardando SMS...{Style.RESET_ALL}")
        else:
            for sms in list(self.sms_buffer)[-10:]:
                # Extrair hora
                try:
                    # Tentar parse ISO format
                    hora = sms['timestamp'].split('T')[1][:5]
                except:
                    hora = datetime.now().strftime("%H:%M")
                
                numero = sms['numero']
                mensagem = sms['mensagem']
                
                # Truncar mensagem longa
                if len(mensagem) > 40:
                    mensagem = mensagem[:37] + "..."
                
                print(f"{Fore.GREEN}[{hora}]{Style.RESET_ALL} {Fore.CYAN}{numero}{Style.RESET_ALL}")
                print(f"       {Fore.WHITE}{mensagem}{Style.RESET_ALL}")
        
        print(f"\n")
        print(f"{Fore.CYAN}{'-'*50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Pressione Ctrl+C para sair{Style.RESET_ALL}")
    
    def rodar(self):
        """Executar monitor"""
        if not self.conectar():
            return
        
        try:
            # Manter vivo enquanto conectado
            while True:
                threading.Event().wait(1)
                if not self.conectado:
                    self.print_status("Tentando reconectar...", Fore.YELLOW)
                    self.conectar()
        
        except KeyboardInterrupt:
            print("\n")
            self.print_status("Encerrando...", Fore.YELLOW)
            if self.conectado:
                self.sio.disconnect()
            sys.exit(0)


def main():
    """Função principal"""
    print(f"{Fore.CYAN}")
    print("╔═════════════════════════════════════════╗")
    print("║  SMS FORWARDER - MONITOR PC             ║")
    print("║  Windows CMD - Tempo Real               ║")
    print("╚═════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}\n")
    
    # Configurar servidor
    servidor = input("URL do Backend [localhost:5000]: ").strip()
    if not servidor:
        servidor = "http://localhost:5000"
    elif not servidor.startswith('http'):
        servidor = f"http://{servidor}"
    
    print("\n")
    
    # Criar e iniciar monitor
    monitor = SMSMonitor(servidor=servidor)
    monitor.rodar()


if __name__ == '__main__':
    main()
