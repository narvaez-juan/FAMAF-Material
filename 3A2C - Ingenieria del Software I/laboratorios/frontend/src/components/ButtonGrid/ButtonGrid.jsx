import Button from "../Button/Button";

const ButtonGrid = ({ buttons }) => {
  const sortedButtons = [...buttons].sort(
    (a, b) => (b.buttonActive === true) - (a.buttonActive === true)
  );

  return (
    <div className="fixed bottom-20 right-6 z-40 w-41 flex flex-col-reverse gap-2">
      {sortedButtons.map(
        (btnProps, index) =>
          btnProps.buttonActive && <Button key={index} {...btnProps} />
      )}
    </div>
  );
};

export default ButtonGrid;
