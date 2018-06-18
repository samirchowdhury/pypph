num_nodes = 20;
A = rand(num_nodes).*(1-eye(num_nodes));

% round to two decimal places
B = zeros(size(A));
for i = 1:size(A,1)
  for j = 1:size(A,2)
    B(i,j) = str2num(sprintf("%.2f", A(i,j)));
  end
end
output_precision(2)




file_id = 1

f = fopen(['randData',num2str(file_id),'.txt'],'w+');
fprintf(f,'%i \r\n',num_nodes);

for i = 1:num_nodes-1
  for j = i+1: num_nodes
    fprintf(f,'%i %i %.2f \r\n', i, j, A(i,j));
    end
    end
    
for i = 2:num_nodes
  for j = 1:i-1
    fprintf(f,'%i %i %.2f \r\n', i, j, A(i,j));
    end
    end

fclose(f);