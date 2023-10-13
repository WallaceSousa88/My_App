// Função para validar o CPF
function validateCPF(cpf) {
    // Implemente a validação do CPF aqui
    // Retorna true se o CPF for válido e false se for inválido
}

// Função para confirmar a exclusão de um usuário
function confirmDelete() {
    if (confirm("Tem certeza de que deseja excluir este usuário?")) {
        return true;
    } else {
        return false;
    }
}

// Função para verificar se todos os campos do formulário de adição estão preenchidos
function validateAddUserForm() {
    var nome = document.getElementById('nome').value;
    var cargo = document.getElementById('cargo').value;
    var departamento = document.getElementById('departamento').value;
    var cpf = document.getElementById('cpf').value;

    if (nome === '' || cargo === '' || departamento === '' || cpf === '') {
        alert('Por favor, preencha todos os campos.');
        return false;
    }

    if (!validateCPF(cpf)) {
        alert('CPF inválido. Por favor, insira um CPF válido.');
        return false;
    }

    return true;
}