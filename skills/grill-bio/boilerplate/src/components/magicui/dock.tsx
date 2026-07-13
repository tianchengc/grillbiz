"use client";
import { cn } from "@/lib/utils";
import { cva, VariantProps } from "class-variance-authority";
import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";
import React, { PropsWithChildren, useRef } from "react";

export interface DockProps extends VariantProps<typeof dockVariants> {
  className?: string;
  iconSize?: number;
  iconMagnification?: number;
  iconDistance?: number;
  direction?: "top" | "middle" | "bottom";
  children: React.ReactNode;
}

const DEFAULT_SIZE = 40;
const DEFAULT_MAGNIFICATION = 60;
const DEFAULT_DISTANCE = 140;

const dockVariants = cva(
  "supports-backdrop-blur:bg-white/10 supports-backdrop-blur:dark:bg-black/10 flex h-[58px] w-max items-end gap-2 rounded-2xl border border-black/10 px-4 pb-3 backdrop-blur-md dark:border-white/10"
);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const DockContext = React.createContext<{
  mouseX: any;
  iconSize: number;
  iconMagnification: number;
  iconDistance: number;
}>({
  mouseX: null,
  iconSize: DEFAULT_SIZE,
  iconMagnification: DEFAULT_MAGNIFICATION,
  iconDistance: DEFAULT_DISTANCE,
});

const Dock = React.forwardRef<HTMLDivElement, DockProps>(
  ({
    className,
    children,
    iconSize = DEFAULT_SIZE,
    iconMagnification = DEFAULT_MAGNIFICATION,
    iconDistance = DEFAULT_DISTANCE,
    direction = "bottom",
    ...props
  }, ref) => {
    const mouseX = useMotionValue(Infinity);
    return (
      <motion.div
        ref={ref}
        onMouseMove={(e) => mouseX.set(e.pageX)}
        onMouseLeave={() => mouseX.set(Infinity)}
        {...props}
        className={cn(dockVariants(), className, {
          "items-start": direction === "top",
          "items-center": direction === "middle",
          "items-end": direction === "bottom",
        })}
      >
        <DockContext.Provider value={{ mouseX, iconSize, iconMagnification, iconDistance }}>
          {children}
        </DockContext.Provider>
      </motion.div>
    );
  }
);
Dock.displayName = "Dock";

const DockIcon = ({ className, children, ...props }: PropsWithChildren<{ className?: string }>) => {
  const ref = useRef<HTMLDivElement>(null);
  const { mouseX, iconSize, iconMagnification, iconDistance } = React.useContext(DockContext);
  const distanceCalc = useTransform(mouseX, (val: number) => {
    const bounds = ref.current?.getBoundingClientRect() ?? { x: 0, width: 0 };
    return val - bounds.x - bounds.width / 2;
  });
  const sizeTransform = useTransform(
    distanceCalc,
    [-iconDistance, 0, iconDistance],
    [iconSize, iconMagnification, iconSize]
  );
  const size = useSpring(sizeTransform, { mass: 0.1, stiffness: 150, damping: 12 });
  return (
    <motion.div
      ref={ref}
      style={{ width: size, height: size }}
      className={cn("flex aspect-square cursor-pointer items-center justify-center rounded-full", className)}
      {...props}
    >
      {children}
    </motion.div>
  );
};
DockIcon.displayName = "DockIcon";

export { Dock, DockIcon, dockVariants };
