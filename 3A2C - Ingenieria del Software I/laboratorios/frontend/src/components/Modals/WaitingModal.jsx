import React from "react";

export default function WaitingModal({ targetName, effect }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
      <div className="bg-slate-900 p-6 rounded-xl shadow-xl w-[400px] border border-yellow-500 text-center">
        <h2 className="text-2xl font-metamorphous text-white mb-4">
          Waiting for {targetName}
        </h2>
        <p className="text-slate-300 font-metamorphous text-base mb-6">
          {targetName} {effect === "REVEAL" ? "" : ""}
          {(() => {
            switch (effect) {
              case "REVEAL":
                return "is choosing which secret to reveal...";
              case "HIDE":
                return "is choosing a secret to hide";
              case "STEAL":
                return "is choosing a secret to steal";
            }
          })()}
        </p>
        <div className="animate-pulse text-yellow-500 text-4xl font-metamorphous">
          ⏳
        </div>
      </div>
    </div>
  );
}
