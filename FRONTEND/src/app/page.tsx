'use client'
import { useContext } from "react";
import { AuthContext } from "@/context/AuthContext";
import ECommerce from "@/components/Dashboard/E-commerce";
import DefaultLayout from "@/components/Layouts/DefaultLayout";
import Loader from "@/components/common/Loader";

export default function Home() {
  const { isAuthenticated } = useContext(AuthContext)


  if (!isAuthenticated) {
    return <Loader />
  }

  

  return (
    <>
      <DefaultLayout>
       
      </DefaultLayout>
    </>
  );
}
