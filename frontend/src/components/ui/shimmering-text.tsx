import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface ShimmeringTextProps {
  text: string
  duration?: number
  className?: string
  wave?: boolean
}

export function ShimmeringText({ 
  text, 
  duration = 2,
  className,
  wave = false
}: ShimmeringTextProps) {
  return (
    <span className={cn('relative inline-block bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 bg-clip-text text-transparent', className)}>
      {text.split('').map((char, index) => (
        <motion.span
          key={index}
          className="inline-block"
          initial={{ opacity: 0.6 }}
          animate={wave ? {
            opacity: [0.6, 1, 0.6],
          } : {
            opacity: [0.6, 1, 0.6],
          }}
          transition={wave ? {
            duration: 2,
            repeat: Infinity,
            delay: index * 0.1,
            ease: 'easeInOut',
          } : {
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
