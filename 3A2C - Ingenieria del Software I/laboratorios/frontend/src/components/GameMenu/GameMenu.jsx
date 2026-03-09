import { useNavigate } from "react-router-dom";

export default function GameMenu({ createGameLink, listGamesLink }) {

    const navigate = useNavigate();

    const goToCreateGame = () => {
        navigate(createGameLink);
    };

    const goToGameList = () => {
        navigate(listGamesLink);
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-950">
        
        <div className="w-full max-w-3xl h-auto p-8 rounded-lg bg-slate-900 shadow-[0_0_4px_#c2a22d]">
            <p className="tracking-wide font-metamorphous text-center text-lg text-[#c2a22d] mb-6">Agatha Christie's</p>
            <h2 className="tracking-wide font-metamorphous text-center text-5xl text-white mb-6">Death on the Cards</h2>
            <p className="tracking-wide font-metamorphous text-center text-sm text-white mb-6">A game of suspicions, secrets... and a bit of betrayal.</p>

            <div className="relative gap-4 flex justify-center">
				<button
					type={"button"}
					className={"font-metamorphous text-center px-10 py-5 text-white rounded-xl focus:outline-none"}
					style={{ background: "#0b3b6f" }}
                    onClick={goToCreateGame}
					onMouseOver={(e) => {	e.currentTarget.style.background = "#c2a22d"; 
											e.currentTarget.style.color = "black" }}
					onMouseOut={(e) => {e.currentTarget.style.background = "#0b3b6f"
											e.currentTarget.style.color = "white"}}
					>
					{"Create Game"}
				</button>

                <button
					type={"button"}
					className={"font-metamorphous text-center px-10 py-5 text-white rounded-xl focus:outline-none"}
					style={{ background: "#0b3b6f" }}
                    onClick={goToGameList}
					onMouseOver={(e) => {	e.currentTarget.style.background = "#c2a22d"; 
											e.currentTarget.style.color = "black" }}
					onMouseOut={(e) => {e.currentTarget.style.background = "#0b3b6f"
											e.currentTarget.style.color = "white"}}
					>
                    {"Join Game"}
				</button>

                <div className="-mx-8 -my-8 absolute bottom-0 left-0 box-border size-15 shadow-[-3px_3px_1px_#c2a22d] rounded-2xl">
                </div>                
                <div className="-mx-8 -my-8 absolute right-0 bottom-0 box-border size-15 shadow-[3px_3px_1px_#c2a22d] rounded-2xl">
                </div>
                <div className="-mx-8 -my-50 absolute top-0 right-0 box-border size-15 shadow-[3px_-3px_1px_#c2a22d] rounded-2xl">
                </div>
                <div className="-mx-8 -my-50 absolute top-0 left-0 box-border size-15 shadow-[-3px_-3px_1px_#c2a22d] rounded-2xl">
                </div>

            </div>



        </div>
    </div>
    );
}