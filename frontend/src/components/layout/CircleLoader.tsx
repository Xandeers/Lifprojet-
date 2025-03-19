import { motion, type Transition } from "framer-motion";

const spinTransition: Transition = {
  repeat: Infinity,
  duration: 1,
  ease: "linear",
};

export default function CircleLoader() {

  return (
    <div className="relative w-20 h-20">
      <motion.span
        className="block w-20 h-20 border-3 border-gray-100 border-t-blue-400 absolute"
        style={{ borderRadius: "50%" }}
        animate={{rotate: 360}}
        transition={spinTransition}
      />
    </div>
  );
}
