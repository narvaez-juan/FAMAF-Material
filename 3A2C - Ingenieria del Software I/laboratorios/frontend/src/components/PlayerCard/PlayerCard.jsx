export default function PlayerCard({ PlayerName }) {
    return (
        <div 
        data-testid="player-card"
        className="relative max-w-[600px] max-h-[95px] p-8 rounded-lg 
        bg-slate-900 shadow-[0_0_4px_#c2a22d]
        hover:shadow-[0_0_15px_#c2a22d] transition-shadow duration-300 ease-in-out">   
            <h2 className="tracking-wide 
                overflow-hidden truncate text-ellipsis
                max-w-[350px] font-metamorphous 
                text-left text-2xl text-white mb-6">
                {PlayerName}
            </h2>
        </div>
    );
}
