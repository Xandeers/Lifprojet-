import {
  ComponentProps,
  createContext,
  PropsWithChildren,
  useCallback,
  useContext,
  useRef,
  useState,
} from "react";
import Toast from "../components/layout/Toast";
import { AnimatePresence, motion } from "framer-motion";

type Params = ComponentProps<typeof Toast> & { duration?: number };
type ToastItem = ComponentProps<typeof Toast> & {
  id: number;
  timer: ReturnType<typeof setTimeout>;
};

const defaultPush = (_toast: Params) => {};

const defaultValue = {
  pushToastRef: { current: defaultPush },
};

const ToastContext = createContext(defaultValue);

export function ToastContextProvider({ children }: PropsWithChildren) {
  const pushToastRef = useRef(defaultPush);
  return (
    <ToastContext.Provider value={{ pushToastRef }}>
      <Toasts />
      {children}
    </ToastContext.Provider>
  );
}

export function useToasts() {
  const { pushToastRef } = useContext(ToastContext);
  return {
    pushToast: useCallback(
      (toast: Params) => {
        pushToastRef.current(toast);
      },
      [pushToastRef]
    ),
  };
}

function Toasts() {
  const [toasts, setToasts] = useState([] as ToastItem[]);
  const { pushToastRef } = useContext(ToastContext);
  pushToastRef.current = ({ duration, ...props }: Params) => {
    const id = Date.now();
    const timer = setTimeout(() => {
      setToasts((v) => v.filter((t) => t != toast));
    }, (duration ?? 5) * 1000);
    const toast = { ...props, id, timer };
    setToasts((v) => [...v, toast]);
  };
  const onRemove = (toast: ToastItem) => {
    clearTimeout(toast.timer);
    setToasts((v) => v.filter((t) => t != toast));
  };
  return (
    <div className="flex flex-col fixed right-4 top-4 gap-3">
      <AnimatePresence>
        {toasts.map((toast: ToastItem) => (
          <motion.div
            onClick={() => onRemove(toast)}
            key={toast.id}
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 30 }}
          >
            <Toast {...toast} />
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
