import Layout from "../../components/layout/Layout.tsx";
import { useAccount } from "../../hooks/useAccount.ts";

export default function MePage() {
  const { account } = useAccount();
  return (
    <Layout>
      <h1>Mon profile</h1>
      {JSON.stringify(account)}
    </Layout>
  )
}