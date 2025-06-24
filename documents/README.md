# 📁 Diretório de Documentos

Coloque seus arquivos PDF e Word (.docx) neste diretório para que o agente possa processá-los.

## Formatos Suportados
- ✅ PDF (.pdf)
- ✅ Word (.docx)
- ❌ Word antigo (.doc) - limitado

## Como Usar

1. **Adicionar Documentos**: Copie seus arquivos para esta pasta
2. **Processar**: Faça uma requisição POST para `/documents/upload`
3. **Consultar**: Use o endpoint `/chat` para fazer perguntas sobre os documentos

## Exemplo de Estrutura
```
documents/
├── manual_usuario.pdf
├── politicas_empresa.docx
├── relatorio_anual.pdf
└── procedimentos.docx
```

## Dicas
- Use nomes descritivos para os arquivos
- Evite caracteres especiais nos nomes
- Documentos grandes podem demorar mais para processar
- O sistema criará chunks dos documentos automaticamente

Após adicionar novos documentos, sempre execute o reprocessamento via API!
