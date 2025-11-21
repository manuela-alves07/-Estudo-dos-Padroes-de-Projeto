# ☕ Sistema de Pedidos de Cafeteria

Sistema desenvolvido para demonstrar a aplicação prática de **4 Padrões de Projeto** em Python.

## 📋 Descrição do Projeto

Este projeto simula um sistema de pedidos de uma cafeteria, permitindo:
- Criar pedidos com diferentes tipos de bebidas
- Adicionar ingredientes extras às bebidas
- Processar pagamentos de diferentes formas
- Acompanhar o status do pedido com notificações

## 🚀 Instruções de Execução

### Pré-requisitos
- Python 3.8 ou superior

### Executando o projeto

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/cafeteria-design-patterns.git

# Entre no diretório
cd cafeteria-design-patterns

# Execute o sistema
python main.py
```

### Saída esperada

O sistema irá demonstrar:
1. Criação de bebidas via Factory
2. Adição de ingredientes via Decorator
3. Processamento de pagamento via Strategy
4. Notificações de status via Observer

## 🎯 Padrões de Projeto Implementados

### 1. Decorator (Estrutural)
**Localização:** `main.py` - linhas 14-62

Permite adicionar ingredientes extras às bebidas de forma dinâmica.

| Classe | Papel |
|--------|-------|
| `Bebida` | Component (interface) |
| `Espresso`, `Cappuccino`, `Latte` | ConcreteComponent |
| `IngredienteDecorator` | Decorator base |
| `Leite`, `Chocolate`, `Chantilly` | ConcreteDecorator |

**Exemplo de uso:**
```python
bebida = Espresso()                    # R$ 5.00
bebida = Leite(bebida)                 # R$ 6.50
bebida = Chocolate(bebida)             # R$ 8.50
print(bebida.descricao())  # "Espresso + Leite + Chocolate"
```

---

### 2. Factory Method (Criacional)
**Localização:** `main.py` - linhas 64-96

Centraliza a criação de bebidas sem expor as classes concretas.

| Classe | Papel |
|--------|-------|
| `BebidaFactory` | Creator (abstrato) |
| `EspressoFactory`, `CappuccinoFactory`, `LatteFactory` | ConcreteCreator |
| `FabricaBebidas` | Simple Factory (fachada) |

**Exemplo de uso:**
```python
bebida = FabricaBebidas.criar("cappuccino")  # Cria Cappuccino
bebida = FabricaBebidas.criar("latte")       # Cria Latte
```

---

### 3. Strategy (Comportamental)
**Localização:** `main.py` - linhas 98-148

Encapsula diferentes algoritmos de pagamento, permitindo troca em runtime.

| Classe | Papel |
|--------|-------|
| `PagamentoStrategy` | Strategy (interface) |
| `PagamentoCartao` | ConcreteStrategy |
| `PagamentoPix` | ConcreteStrategy |
| `PagamentoDinheiro` | ConcreteStrategy |
| `Pedido` | Context |

**Exemplo de uso:**
```python
pedido.definir_pagamento(PagamentoPix("email@pix.com"))
pedido.processar_pagamento()

# Ou trocar para cartão
pedido.definir_pagamento(PagamentoCartao("1234567890123456"))
pedido.processar_pagamento()
```

---

### 4. Observer (Comportamental)
**Localização:** `main.py` - linhas 150-192

Notifica automaticamente múltiplos sistemas quando o status do pedido muda.

| Classe | Papel |
|--------|-------|
| `Pedido` | Subject (Observable) |
| `ObservadorPedido` | Observer (interface) |
| `NotificadorCliente` | ConcreteObserver |
| `PainelPedidos` | ConcreteObserver |
| `SistemaMetricas` | ConcreteObserver |

**Exemplo de uso:**
```python
pedido.adicionar_observer(NotificadorCliente("João"))
pedido.adicionar_observer(PainelPedidos())

pedido.status = StatusPedido.PRONTO  # Notifica todos os observers
```

## 📁 Estrutura do Projeto

```
cafeteria-design-patterns/
│
├── main.py          # Código-fonte principal
├── README.md        # Este arquivo
└── RESUMO.md        # Estudo teórico dos padrões
```

## 📚 Documentação Adicional

Para o estudo teórico completo dos padrões, incluindo:
- Descrição detalhada de cada padrão
- Trade-offs e quando utilizar
- Comparações entre padrões
- Variações de implementação

Consulte o arquivo [RESUMO.md](./RESUMO.md)

## 🔗 Referências

- [Refactoring.Guru - Design Patterns](https://refactoring.guru/pt-br/design-patterns)
