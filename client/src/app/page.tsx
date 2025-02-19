import Image from "next/image";
import StartGameButton from "./_components/StartGameButton";
import CheckCodeButton from "./_components/CheckCodeButton";
import Footer from "./_components/Footer";
import App from "./_components/App";

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <App>
          <div className="h1 text-6xl self-center"> Minesweeper </div>
          <div className="flex gap-4 items-center flex-col sm:flex-row">
            <StartGameButton />
            <CheckCodeButton />
          </div>
        </App>
      </main>
      <Footer />
    </div>
  );
}
