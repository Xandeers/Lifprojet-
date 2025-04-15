import { useParams } from "react-router";
import Layout from "../../components/layout/Layout.tsx";

export default function RecipePage() {
  const { slug } = useParams();
  return <Layout>{slug}</Layout>;
}
