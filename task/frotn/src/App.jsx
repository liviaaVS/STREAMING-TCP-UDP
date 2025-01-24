import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";
import { useForm } from "react-hook-form";

export let tarefas = []; // Corrigir a declaração da variável tarefas

function App() {
  const { register, handleSubmit } = useForm();
  const [taref, setTarefas] = useState([]);
  async function onSubmit(data) {
    setTarefas([...tarefas, data]);
    tarefas = [...taref, data];
  }

  return (
    <div className="App">
      <div className="container mt-5">
        <h2>Cadastrar Tarefa</h2>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="mb-3">
            <label htmlFor="nome" className="form-label">
              Nome da Tarefa
            </label>
            <input
              type="text"
              className="form-control"
              id="nome"
              {...register("nome", { required: true })}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="descricao" className="form-label">
              Descrição
            </label>
            <textarea
              className="form-control"
              id="descricao"
              rows="3"
              {...register("descricao", { required: true })}
            ></textarea>
          </div>
          <button type="submit" className="btn btn-primary">
            Cadastrar Tarefa
          </button>
        </form>

        <br />
        <br />
        <h2>Listando Tarefas</h2>
        <ul className="list-group">
          {tarefas.length === 0 ? (
            <li className="list-group-item">Nenhuma tarefa cadastrada</li>
          ) : (
            <div>
              {" "}
              {tarefas.map((tarefa) => (
                <li key={tarefa.id} className="list-group-item">
                  <h3>{tarefa.nome}</h3>
                  <p>{tarefa.descricao}</p>
                </li>
              ))}
            </div>
          )}
        </ul>
      </div>
    </div>
  );
}

export default App;
