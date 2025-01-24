const protoLoader = require("@grpc/proto-loader");
const grpc = require("@grpc/grpc-js");
const readline = require("readline");

const packageDefinition = protoLoader.loadSync("tarefa.proto", {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});
const tasksProto = grpc.loadPackageDefinition(packageDefinition).TaskService;
console.log(tasksProto);
const client = new tasksProto(
  "localhost:50051",
  grpc.credentials.createInsecure()
);

// Criando a interface de leitura
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function CreateTask(tarefas) {
  client.CreateTask(tarefas, (error, response) => {
    if (error) console.error("Error:", error);
    else return response.result;
  });
}

rl.question("Qual é o nome da tarefa? ", (nome) => {
  rl.question("Qual é a descrição da tarefa? ", (descricao) => {
    const tarefa = { nome, descricao };
    console.log(tarefa);
    console.log(CreateTask(tarefa));
    rl.close();
  });
});
