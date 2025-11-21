# Padrões de Arquitetura

## Introdução

Este documento apresenta o estudo teórico dos padrões de projeto utilizados no **Sistema de Pedidos de Cafeteria**, desenvolvido como parte da atividade prática de Padrões de Arquitetura de Software.

Os padrões foram estudados através da plataforma [Refactoring.Guru](https://refactoring.guru/pt-br/design-patterns) e aplicados em um contexto real de desenvolvimento.

---

## 1. Decorator (Estrutural)

### 1.1 Propósito
O padrão Decorator permite adicionar novos comportamentos a objetos dinamicamente, colocando-os dentro de objetos "wrapper" que contêm esses comportamentos. É uma alternativa flexível à herança para estender funcionalidades.

### 1.2 Problema que Resolve
Quando precisamos adicionar responsabilidades a objetos individuais (não a uma classe inteira) de forma dinâmica e transparente, sem afetar outros objetos. A herança é estática e se aplica a toda a classe, o que pode levar a uma explosão de subclasses.

### 1.3 Estrutura
- **Component**: Interface comum para wrappers e objetos concretos
- **ConcreteComponent**: Objeto que terá comportamentos adicionados
- **Decorator**: Classe base abstrata que mantém referência ao componente
- **ConcreteDecorator**: Adiciona comportamentos específicos

### 1.4 Quando Utilizar
- Quando você precisa adicionar responsabilidades a objetos em tempo de execução
- Quando a extensão por herança é impraticável ou impossível
- Quando você quer combinar vários comportamentos de forma flexível

### 1.5 Trade-offs
| Vantagens | Desvantagens |
|-----------|--------------|
| Maior flexibilidade que herança | Muitos objetos pequenos podem dificultar debug |
| Responsabilidade única (SRP) | Ordem dos decorators pode importar |
| Composição de comportamentos | Código inicial mais complexo |

### 1.6 Aplicação no Projeto
No sistema de cafeteria, o Decorator é usado para adicionar ingredientes extras às bebidas (leite, chocolate, chantilly). Cada ingrediente é um decorator que envolve a bebida base e adiciona seu custo e descrição.

---

## 2. Factory Method (Criacional)

### 2.1 Propósito
O Factory Method define uma interface para criar objetos, mas permite que as subclasses decidam qual classe instanciar. Ele delega a instanciação para subclasses.

### 2.2 Problema que Resolve
Quando o código precisa trabalhar com diversas famílias de produtos relacionados, mas você não quer que ele dependa das classes concretas desses produtos. O Factory Method desacopla o código de criação do código de uso.

### 2.3 Estrutura
- **Product**: Interface comum dos objetos criados
- **ConcreteProduct**: Implementações específicas do produto
- **Creator**: Declara o factory method (pode ter implementação padrão)
- **ConcreteCreator**: Sobrescreve o factory method para retornar produto específico

### 2.4 Quando Utilizar
- Quando você não sabe de antemão os tipos exatos de objetos que seu código vai trabalhar
- Quando você quer fornecer uma forma de estender componentes internos
- Quando você quer economizar recursos reutilizando objetos existentes

### 2.5 Trade-offs
| Vantagens | Desvantagens |
|-----------|--------------|
| Evita acoplamento forte | Pode haver muitas subclasses |
| Princípio aberto/fechado | Complexidade adicional |
| Princípio da responsabilidade única | - |

### 2.6 Aplicação no Projeto
A fábrica de bebidas cria diferentes tipos de café (Espresso, Cappuccino, Latte) sem que o código cliente precise conhecer as classes concretas. Isso permite adicionar novos tipos de bebidas facilmente.

---

## 3. Strategy (Comportamental)

### 3.1 Propósito
O Strategy define uma família de algoritmos, encapsula cada um deles e os torna intercambiáveis. Permite que o algoritmo varie independentemente dos clientes que o utilizam.

### 3.2 Problema que Resolve
Quando você tem múltiplas formas de realizar uma mesma operação e precisa escolher entre elas em tempo de execução. Evita condicionais extensos (if/else ou switch) para selecionar comportamentos.

### 3.3 Estrutura
- **Strategy**: Interface comum para todos os algoritmos
- **ConcreteStrategy**: Implementações específicas de cada algoritmo
- **Context**: Mantém referência para uma Strategy e delega o trabalho

### 3.4 Quando Utilizar
- Quando você tem muitas classes similares que diferem apenas no comportamento
- Quando você precisa isolar a lógica de negócio de detalhes de implementação
- Quando você tem um condicional massivo que seleciona variantes do mesmo algoritmo

### 3.5 Trade-offs
| Vantagens | Desvantagens |
|-----------|--------------|
| Troca de algoritmos em runtime | Cliente deve conhecer as diferenças |
| Isola código e dados dos algoritmos | Pode ser overkill para poucos algoritmos |
| Princípio aberto/fechado | Lambdas podem substituir em casos simples |

### 3.6 Aplicação no Projeto
As estratégias de pagamento (Cartão de Crédito, PIX, Dinheiro) são implementadas como strategies. O sistema de pedidos pode processar qualquer forma de pagamento sem conhecer os detalhes de cada uma.

---

## 4. Observer (Comportamental)

### 4.1 Propósito
O Observer define uma dependência um-para-muitos entre objetos, de modo que quando um objeto muda de estado, todos os seus dependentes são notificados e atualizados automaticamente.

### 4.2 Problema que Resolve
Quando a mudança de estado de um objeto requer mudanças em outros objetos, e o conjunto real de objetos é desconhecido ou muda dinamicamente. Evita acoplamento forte entre objetos relacionados.

### 4.3 Estrutura
- **Subject/Publisher**: Mantém lista de observers e notifica sobre mudanças
- **Observer/Subscriber**: Interface para objetos que devem ser notificados
- **ConcreteObserver**: Implementa a interface e reage às notificações

### 4.4 Quando Utilizar
- Quando mudanças em um objeto requerem mudanças em outros
- Quando um objeto deve notificar outros sem fazer suposições sobre quem são
- Quando você precisa de um sistema de eventos/notificações

### 4.5 Trade-offs
| Vantagens | Desvantagens |
|-----------|--------------|
| Princípio aberto/fechado | Subscribers notificados em ordem aleatória |
| Estabelece relações em runtime | Pode haver memory leaks se não desinscrever |
| Desacoplamento entre objetos | Atualizações em cascata podem ser complexas |

### 4.6 Aplicação no Projeto
Quando um pedido muda de status (preparando → pronto), todos os observadores interessados são notificados: o cliente recebe aviso, o painel de pedidos atualiza, o sistema de métricas registra.

---

## Comparações entre os Padrões

### Semelhanças
- **Decorator e Strategy**: Ambos usam composição em vez de herança para adicionar flexibilidade
- **Factory e Strategy**: Ambos encapsulam código que varia, facilitando extensão
- **Observer e Strategy**: Ambos promovem baixo acoplamento entre componentes

### Diferenças Fundamentais
| Aspecto | Decorator | Factory | Strategy | Observer |
|---------|-----------|---------|----------|----------|
| Categoria | Estrutural | Criacional | Comportamental | Comportamental |
| Foco | Adicionar responsabilidades | Criar objetos | Variar algoritmos | Notificar mudanças |
| Relação | Wrapper/Wrapped | Creator/Product | Context/Strategy | Subject/Observer |

### Combinações Possíveis
1. **Factory + Decorator**: Factory cria objetos base, Decorator os enriquece
2. **Strategy + Factory**: Factory cria strategies baseado em configuração
3. **Observer + Strategy**: Observers podem usar strategies para processar notificações

---

## Iterações e Variações

### Decorator
- **Variação clássica**: Decorators herdam da mesma interface do componente
- **Variação funcional**: Usar funções de ordem superior (closures) como decorators
- **Python específico**: Decorators com `@` syntax para funções/métodos

### Factory Method
- **Simple Factory**: Não é um padrão GoF, mas uma simplificação comum
- **Abstract Factory**: Extensão para famílias de objetos relacionados
- **Factory com registro**: Usar dicionário para mapear tipos a classes

### Strategy
- **Strategy com lambdas**: Em linguagens funcionais, strategies podem ser funções
- **Strategy com injeção**: Injetar strategy via construtor ou setter
- **Null Strategy**: Strategy que não faz nada (evita null checks)

### Observer
- **Push model**: Subject envia dados detalhados na notificação
- **Pull model**: Observers consultam subject após notificação
- **Event-driven**: Usar sistemas de eventos mais elaborados

---

## Referências

- Refactoring.Guru - Design Patterns. Disponível em: https://refactoring.guru/pt-br/design-patterns
