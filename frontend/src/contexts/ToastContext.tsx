import { ComponentProps, createContext, PropsWithChildren, useCallback, useContext, useRef, useState } from "react";
import Toast from "../components/toast/Toast";
import { AnimatePresence, motion } from "framer-motion";

type Params = ComponentProps<typeof Toast> & {duration?: number};

const defaultPush = (_toast: Params) => {};

const defaultValue = {
    pushToastRef: {current: defaultPush}
};

const ToastContext = createContext(defaultValue);

export function ToastContextProvider({children}: PropsWithChildren) {
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
        pushToast: useCallback((toast: Params) => {
            pushToastRef.current(toast);
        }, [pushToastRef])
    }
}

function Toasts() {
    const [toasts, setToasts] = useState([] as Params[]);
    const { pushToastRef } = useContext(ToastContext);
    pushToastRef.current = ({duration, ...toast}: Params) => {
        setToasts(v => [...v, toast]);
        if (duration) {
            setTimeout(() => {
                setToasts((v) => v.filter(t => t != toast ));
            }, duration * 1000);
        }
    };
    return (
        <div>
            <AnimatePresence>
                {toasts.map((toast: Params, k) =>
                    <motion.div
                        key={k}
                        initial={{ opacity: 0, x: -30 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 30 }}
                    >
                        <Toast {...toast} />
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}