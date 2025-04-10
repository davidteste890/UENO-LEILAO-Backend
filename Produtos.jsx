import { useEffect, useState } from "react";
import axios from "axios";

export default function Produtos() {
  const [produtos, setProdutos] = useState([]);
  const [valores, setValores] = useState({});

  useEffect(() => {
    axios.get("http://localhost:5000/api/produtos")
      .then(res => setProdutos(res.data))
      .catch(err => console.error("Erro ao buscar produtos:", err));
  }, []);

  const handleLance = async (produtoId) => {
    const token = localStorage.getItem("token");
    const valor = valores[produtoId];

    if (!valor) {
      alert("Informe um valor para o lance.");
      return;
    }

    try {
      await axios.post("http://localhost:5000/api/lance", {
        produto_id: produtoId,
        valor: parseFloat(valor)
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      alert("Lance enviado com sucesso!");
      setValores((prev) => ({ ...prev, [produtoId]: "" }));
    } catch (err) {
      alert("Erro ao enviar o lance. Verifique se está logado.");
      console.error(err);
    }
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold text-center text-green-700 mb-6">Produtos em Leilão</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {produtos.map((produto) => (
          <div key={produto.id} className="bg-white shadow-md rounded-2xl p-6 border border-green-300">
            <h2 className="text-xl font-bold text-green-800">{produto.nome}</h2>
            <p className="text-gray-700">{produto.descricao}</p>
            <p className="text-green-600 font-semibold mt-2">Lance inicial: R$ {produto.preco_inicial.toFixed(2)}</p>

            <div className="mt-4 flex flex-col sm:flex-row items-center gap-2">
              <input
                type="number"
                placeholder="Valor do lance"
                value={valores[produto.id] || ""}
                onChange={(e) =>
                  setValores((prev) => ({ ...prev, [produto.id]: e.target.value }))
                }
                className="border border-green-300 rounded-xl px-3 py-1 w-full sm:w-auto"
              />
              <button
                onClick={() => handleLance(produto.id)}
                className="bg-green-600 hover:bg-green-700 text-white font-bold py-1.5 px-4 rounded-xl"
              >
                Dar Lance
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
