import textwrap
from datetime import datetime
from abc import ABC, abstractmethod

class Conta:
    def __init__(self, numero,  cliente ): #agencia, conta
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self): # retorna um float
        return self._saldo
   
    @classmethod
    def nova_conta(cls, numero_conta, cliente): #agencia
        return cls(numero_conta, cliente) #retorna um objeto Conta


    def sacar(self, valor):

        if valor > self._saldo: #excede saldo
            print("\n >>> Erro ao processar a operação. Não há saldo suficiente.")
            

        elif valor > 0:
            self._saldo -= valor 
            print("\n >>> Operação realizada com sucesso!")
            return True
        
        else:
            print("\n>>> Erro ao processar a operação. Valor de saque inválido.")
            
        return False #retorna um bool


    def depositar(self, valor):
        
        if valor > 0:
            self._saldo += valor #não por self.saldo em var
            print("\n>>> Operação realizada com sucesso!")
            return True
        
        else:
            print("\n>>> Erro ao processar a operação. Valor de depósito inválido.")
        
        return False


    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    

#classe filha da classe Conta
class ContaCorrente(Conta):
    def __init__(self, numero, cliente): #saldo, agencia, historico, conta
        super().__init__(numero,cliente)
        self.limite = 500
        self.limite_saques = 3
        self.numero_saques = 0
        

    def sacar(self, valor):
        for transacao in self.historico.transacoes:
            if transacao["tipo"] == "Saque":
                self.numero_saques += 1

        # numero_saques = len(
        #     [transacao for transacao in self.historico.transacoes
        #     if transacao["tipo"] ==Saque.__name__] 
        # )

        if self.numero_saques > self.limite_saques:
            print("\n>>> Erro ao processar a operação. Limite de saques excedido.")
  
        elif valor > self.limite:
            print("\n>>> Erro ao processar a operação. Valor de saque excede o limite.")
            
        else:
            return super().sacar(valor)
            
        return False
        
    # def __str__(self):
    #     return f"""\
    #         Agência: \t{self.agencia}
    #         C/C:\t\t{self.numero}
    #         Titular:\t{self.cliente.nome}
    #     """
 

class Historico:
    def __init__(self):
        self._transacoes = []
        

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                # "data": datetime.now().strftime
                # ("%d-%m-%Y %H:%M:%s"),

            }
        )

    @property
    def transacoes(self):
        return self._transacoes



class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar_conta(self, conta):
        pass

    

class Saque(Transacao):
    # def __init__(self, conta, valor):
    #     super().__init__(conta)
    #     self.valor = valor

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar_conta(self, conta):  #mesmo nome de função declarado na classe Transacao
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


 
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor


    @property
    def valor (self):
        return self._valor

    def registrar_conta (self, conta): #mesmo nome de função declarado na classe Transacao
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

                              
                   
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar_conta(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
        

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
    




def menu_principal():
    menu_principal = """
------------------ MENU ------------------
    
    [n] Cadastrar Novo Usuario
    [cc] Cadastrar Nova Conta Corrente

    [d] Depositar
    [s] Sacar
    [e] Extrato
        
    [q] Sair

    =>"""
    return input(menu_principal)

def menu_conta():
    menu_conta = """
------------------ MENU ------------------
    
    
    =>"""
    return input(menu_conta)


def sacar(clientes):
    cliente = acessar_cliente(clientes)
    if not cliente: 
        return
    
    conta = recuperar_conta(cliente)
    if not conta:
        return
            
    valor_saque = float(input("Insira o valor do saque: "))
    transacao = Saque(valor_saque)

    cliente.realizar_transacao(conta, transacao)



def depositar(clientes):
    cliente = acessar_cliente(clientes)
    if cliente:
        conta = recuperar_conta(cliente)

        if conta: 
            valor_deposito = float(input("Insira o valor do depósito: "))
            transacao = Deposito(valor_deposito)

            cliente.realizar_transacao(conta, transacao)

    return

def imprimir_extrato(clientes):
    cliente = acessar_cliente(clientes)
    if not cliente:
        return
    conta = recuperar_conta(cliente)
    
    if not conta:
        return 
    
    conta = recuperar_conta(cliente)
    print("\n================= EXTRATO =================")
    transacoes = conta.historico.transacoes

    extrato = ""

    if not transacoes:
        print("\n >>> Não foram realizadas movimentações. \n\n===========================================")

    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']:<25} R$ {transacao['valor']:>10.2f}"

        print(extrato)
        print("\n===========================================")
        print(f"{'Saldo':<25} R$ {conta.saldo:>10.2f}")
        print("===========================================")


def criar_usuario(clientes):
    cpf = int(input("Informe CFP (apenas números): "))
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n>>> Usuário já cadastrado!")
        return


    nome = input("Nome Completo: ").strip()
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ").strip()
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, endereco=endereco, cpf=cpf)
    clientes.append(cliente)

    print("\n>>> Cliente cadastrado com sucesso.")

    # return clientes


def criar_conta_corrente(clientes, contas, numero_conta):
    cliente = acessar_cliente(clientes)
    if not cliente:
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero_conta=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print("\n>>> Conta criada com sucesso.")
    


def filtrar_cliente(cpf, clientes):
    # Resolução avançada - inline
    # clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    # return clientes_filtrados[0] if clientes_filtrados else None
    
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente  # Encontrou o cliente, retorna ele
    return None  # Nenhum cliente encontrado com esse CPF


def recuperar_conta(cliente):
    if not cliente.contas:
        print("\n >>> Cliente não possui conta.")
        return
    
    #A conta retornada é sempre a primeira, sem opção de escolher a conta
    return cliente.contas[0]


def acessar_cliente(clientes):
    cpf = int(input("Informe CFP (apenas números): "))
    usuario = filtrar_cliente(cpf, clientes)

    if not usuario:
        print("\n >>> Cliente não localizado.")
        return

    return usuario

# def listar_contas(contas):
#     for conta in contas:
#         print("=" * 100)
#         print(textwrap.dedent(str(conta)))

           
def main():

    clientes = []
    contas = []

    while True:

        opcao = menu_principal()

        if opcao == "n":
            criar_usuario(clientes)
            
        elif opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            imprimir_extrato(clientes)

        elif opcao == "cc":
            numero_conta = len(contas) + 1
            criar_conta_corrente(clientes, contas, numero_conta)
              
        # elif opcao == "l":
        #     listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print(
                "\n>>> Operação inválida, por favor selecione novamente a operação desejada."
            )


main()
