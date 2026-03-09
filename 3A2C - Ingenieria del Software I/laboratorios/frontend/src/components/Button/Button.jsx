const Button = ({
  buttonColor,
  buttonHoverColor,
  className = "text-white",
  onDisabledHandler,
  onClickHandler,
  buttonText,
}) => {
  return (
    <button
      className={`font-metamorphous px-5 py-3 rounded-xl shadow-[0_0_6px_#c2a22d] z-40 ${className}`}
      style={{ background: `${buttonColor}` }}
      onMouseOver={(e) => {
        e.currentTarget.style.background = `${buttonHoverColor}`;
        e.currentTarget.style.color = "black";
      }}
      onMouseOut={(e) => {
        e.currentTarget.style.background = `${buttonColor}`;
        e.currentTarget.style.color = "white";
      }}
      disabled={onDisabledHandler}
      onClick={onClickHandler}
    >
      {buttonText}
    </button>
  );
};

export default Button;
