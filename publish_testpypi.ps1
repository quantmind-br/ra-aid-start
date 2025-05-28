# Script para construir e publicar o pacote ra-aid-start no TestPyPI

# Exibe uma mensagem inicial
Write-Host "Iniciando o processo de build e publicação para o TestPyPI..."

# 1. Construir o pacote
Write-Host "Passo 1: Construindo o pacote com 'poetry build'..."
poetry build
if ($LASTEXITCODE -ne 0) {
    Write-Error "Erro durante o 'poetry build'. Verifique a saída acima."
    exit 1
}
Write-Host "Build concluído com sucesso."
Write-Host ""

# 2. Publicar no TestPyPI
Write-Host "Passo 2: Publicando o pacote no TestPyPI com 'poetry publish -r test-pypi'..."
Write-Host "Certifique-se de que você está autenticado no TestPyPI e que a versão foi incrementada."
poetry publish -r test-pypi
if ($LASTEXITCODE -ne 0) {
    Write-Error "Erro durante o 'poetry publish -r test-pypi'. Verifique a saída acima."
    exit 1
}
Write-Host "Publicação no TestPyPI concluída com sucesso!"
Write-Host ""
Write-Host "Processo finalizado."