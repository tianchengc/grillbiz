import { ReactNode } from "react";
import { cn } from "@/lib/utils";

export const BentoGrid = ({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) => {
  return (
    <div className={cn("grid w-full auto-rows-[22rem] grid-cols-3 gap-4", className)}>
      {children}
    </div>
  );
};

export const BentoCard = ({
  name,
  className,
  background,
  Icon,
  description,
  href,
  cta,
}: {
  name: string;
  className: string;
  background?: ReactNode;
  Icon: any;
  description: string;
  href?: string;
  cta?: string;
}) => (
  <div
    key={name}
    className={cn(
      "group relative col-span-3 flex flex-col justify-between overflow-hidden rounded-xl border border-neutral-200 bg-white/85 transition-all duration-300 hover:shadow-md hover:border-neutral-400",
      className
    )}
  >
    <div className="absolute inset-0 -z-10">{background}</div>
    
    <div className="flex flex-1 flex-col justify-between p-6">
      <div className="flex flex-col gap-1">
        <Icon className="h-8 w-8 text-neutral-800 transition-transform duration-300 group-hover:scale-110" />
        <h3 className="text-lg font-bold text-neutral-900 mt-4">
          {name}
        </h3>
        <p className="max-w-lg text-neutral-500 text-sm leading-relaxed mt-2">{description}</p>
      </div>

      {href && cta && (
        <div className="mt-6">
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-neutral-900 hover:text-neutral-600 transition-colors"
          >
            <span>{cta}</span>
            <svg className="h-3.5 w-3.5 transition-transform duration-350 group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
            </svg>
          </a>
        </div>
      )}
    </div>
  </div>
);
