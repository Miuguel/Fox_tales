function updated_matrix = update_matrix(matrix, num_iterations, variacao)
    % Função para atualizar a matriz
    % matrix: matriz inicial
    % num_iterations: número de iterações
    % variacao: fator de variação pequeno

    [rows, cols] = size(matrix); % Tamanho da matriz

    for iter = 1:num_iterations
        % Criar matrizes deslocadas
        matrix_up = [matrix(2:end, :); zeros(1, cols)];
        matrix_down = [zeros(1, cols); matrix(1:end-1, :)];
        matrix_left = [matrix(:, 2:end) zeros(rows, 1)];
        matrix_right = [zeros(rows, 1) matrix(:, 1:end-1)];
        
        % Soma das matrizes deslocadas
        sum_neighbors = matrix_up + matrix_down + matrix_left + matrix_right;
        
        % Número de vizinhos válidos
        num_neighbors = (matrix_up ~= 0) + (matrix_down ~= 0) + (matrix_left ~= 0) + (matrix_right ~= 0);
        
        % Evitar divisão por zero
        num_neighbors(num_neighbors == 0) = 1;
        
        % Calcular a nova matriz com a fórmula fornecida
        new_matrix = matrix + variacao * (sum_neighbors ./ num_neighbors - matrix);
        
        % Atualizar a matriz original com a nova matriz
        matrix = new_matrix;
    end

    updated_matrix = matrix; % Retornar a matriz atualizada
end


% Exemplo de uso:
initial_matrix = [1 2 3; 4 5 6; 7 8 9];
num_iterations = 5;
variacao = 0.1; % Valor pequeno para a variação

% Iniciar o cronômetro
tic;

% Executar a função
result = update_matrix(initial_matrix, num_iterations, variacao);

% Parar o cronômetro e exibir o tempo decorrido
elapsed_time = toc;
disp('Updated Matrix:');
disp(result);
fprintf('Elapsed time: %.4f seconds\n', elapsed_time);
