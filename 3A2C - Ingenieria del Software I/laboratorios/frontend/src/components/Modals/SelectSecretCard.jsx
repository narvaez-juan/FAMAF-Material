import React, { useState } from "react";
import Secret from "../Secret/Secret";

export default function SelectSecretCardModal({
  effect,
  secrets,
  isOwner,
  onConfirm,
}) {
  const [selectedId, setSelectedId] = useState(null);

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/80 backdrop-blur-sm" />

      <div className="relative w-full max-w-4xl max-h-[84vh] overflow-hidden rounded-2xl shadow-2xl border border-gray-700 z-50">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-900 to-black px-6 py-5 border-b border-yellow-400">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-md bg-gradient-to-br from-[#112b57] to-[#0b3b6f] flex items-center justify-center shadow-[0_0_4px_#c2a22d]">
                <span className="text-3xl font-metamorphous font-bold text-[#c2a22d]">
                  ?
                </span>
              </div>
              <div>
                <h3 className="text-xl font-metamorphous font-bold text-white leading-none">
                  {(() => {
                    switch (effect) {
                      case "REVEAL":
                        return "Choose a secret to reveal";
                      case "HIDE":
                        return "Choose a secret to hide";
                      case "STEAL":
                        return "Choose a secret to steal";
                    }
                  })()}
                </h3>
              </div>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="bg-slate-900 px-6 py-6 overflow-auto max-h-[calc(84vh-180px)]">
          {secrets.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 justify-items-center">
              {secrets.map((secret) => {
                const canSelect =
                  (effect === "REVEAL" && !secret.isRevealed) ||
                  (effect === "HIDE" && secret.isRevealed) ||
                  effect === "STEAL";
                return (
                  <div
                    key={secret.id}
                    onClick={() => canSelect && setSelectedId(secret.id)}
                    className={`flex flex-col items-center transform transition-transform hover:-translate-y-1 cursor-pointer ${
                      selectedId === secret.id
                        ? "ring-2 ring-yellow-500 scale-105"
                        : ""
                    }`}
                  >
                    <Secret
                      image={secret.image}
                      alt="Secret"
                      isRevealed={isOwner ? true : secret.isRevealed}
                    />
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-12 text-gray-400 font-metamorphous">
              No secrets available
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-slate-950 px-6 py-4 flex flex-col sm:flex-row-reverse items-center gap-3 border-t border-gray-800">
          <button
            onClick={() => onConfirm(selectedId)}
            disabled={!selectedId}
            className={`inline-flex items-center justify-center rounded-xl px-6 py-2 text-sm font-metamorphous font-semibold shadow-[0_0_6px_#c2a22d] transition-all
              ${
                selectedId
                  ? "bg-[#c2a22d] text-black hover:brightness-95"
                  : "bg-gray-700 text-gray-400 cursor-not-allowed"
              }`}
          >
            {(() => {
              switch (effect) {
                case "REVEAL":
                  return "Reveal";
                case "HIDE":
                  return "Hide";
                case "STEAL":
                  return "Steal";
              }
            })()}
          </button>
        </div>
      </div>
    </div>
  );
}
