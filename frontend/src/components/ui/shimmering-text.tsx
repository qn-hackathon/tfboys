import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface ShimmeringTextProps {
  text: string
  duration?: number
  className?: string
}

export function ShimmeringText({ 
  text, 
  duration = 2,
  className 
}: ShimmeringTextProps) {
  return (
    <span className={cn('relative inline-block', className)}>
      {text.split('').map((char, index) => (
        <motion.span
          key={index}
          className="inline-block"
          initial={{ opacity: 0.6 }}
          animate={{
            opacity: [0.6, 1, 0.6],
          }}
          transition={{
            duration: duration,
            repeat: Infinity,
            delay: index * 0.1,
            ease: 'easeInOut',
          }}
        >
          {char === ' ' ? '\u00A0' : char}
        </motion.span>
      ))}
    </span>
  )
}
