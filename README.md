# Prática: Testes Unitários + CI/CD

## Instruções

1. Faça o fork do repositório:
   https://github.com/guilherme-augusto-ferraz/desafio-teste-unitario-ci-cd

2. Analise o funcionamento do sistema (CRUD de tarefas).

---

## Definição de cenários de teste

Antes de implementar os testes, defina cenários como:

- Criar tarefa com nome válido → resultado esperado: sucesso
- Criar tarefa com nome vazio → resultado esperado: erro
- Remover tarefa com ID válido → resultado esperado: sucesso
- Remover tarefa com ID inexistente → resultado esperado: erro

considerando:
- Casos de sucesso
- Casos de erro
- Casos limite

---

## Implementação dos testes

3. Crie testes unitários para os cenários definidos.

Você pode utilizar ferramentas de IA como:
- ChatGPT
- GitHub Copilot
- Gemini
- Etc.

Importante:
- Revise os testes gerados
- Garanta que eles realmente validam o comportamento esperado

---

## CI/CD com GitHub Actions

4. Configure uma pipeline de CI/CD para executar os testes automaticamente:

- A pipeline deve rodar a cada **push**
- Os testes devem ser executados automaticamente
- O resultado deve ser visível na aba **Actions** do repositório

---

## Validação

6. Faça um commit e push com os testes implementados.

7. Verifique se:
- A pipeline executa corretamente
- Os testes passam (ou falham, se houver erro)

---

## Opcional – extra

- Quebre propositalmente uma funcionalidade e observe o comportamento da pipeline
- Adicione novos cenários de teste
- Inclua badge de status no README

---

## Entrega

- Link do repositório forkado
- Testes implementados
- Pipeline configurada e funcionando
- Demonstração em aula
