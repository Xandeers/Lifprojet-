import useSWR, { mutate } from "swr";
import endpoints from "../utils/api";

const fetcher = (url: RequestInfo) => fetch(url).then((res) => res.json());

type ProductNutrients = {
    calories: number;
    sodium: number;
    total_fat: number;
    total_sugars: number;
};

type Product = {
    id: number;
    name: string;
    category: string;
    nutrients: Array<ProductNutrients>;
};

const ProductList = () => {
    const { data, error, isLoading } = useSWR<Product[]>(endpoints.products, fetcher);
    
    const handleRefresh = () => {
        mutate(endpoints.products);
    };
    
    if (isLoading) return <div>Chargement...</div>;
    if (error) return <div>Erreur: {error.message}</div>
    
    if (!Array.isArray(data)) return <div>Les données ne sont pas un tableau</div>
    
    return (
        <>
        <h2>Produits:</h2>
        <button
        onClick={handleRefresh}
        >
        Rafraichir
        </button>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
        <tr>
        {Object.keys(data[0]).map((key) => (
            <th
            key={key}
            style={{
                border: '1px solid #ddd',
                padding: '8px',
                backgroundColor: '#f4f4f4',
                textAlign: 'left',
            }}
            >
            {key}
            </th>
        ))}
        </tr>
        </thead>
        <tbody>
        {/* Rendre les lignes */}
        {data.map((item) => (
            <tr key={item.id}>
            {Object.values(item).map((value, index) => (
                <td
                key={index}
                style={{
                    border: '1px solid #ddd',
                    padding: '8px',
                }}
                >
                {typeof value === 'object' ? JSON.stringify(value) : value}
                </td>
            ))}
            </tr>
        ))}
        </tbody>
        </table>
        </>
    )
};

export default ProductList;