import Link from 'next/link'
import styles from './Button.module.css'

interface ButtonProps {
  children: React.ReactNode
  href?: string
  variant?: 'primary' | 'secondary' | 'outline'
  onClick?: () => void
  type?: 'button' | 'submit'
  className?: string
}

export default function Button({ 
  children, 
  href, 
  variant = 'primary', 
  onClick,
  type = 'button',
  className: externalClassName
}: ButtonProps) {
  const className = `${styles.button} ${styles[variant]}${externalClassName ? ` ${externalClassName}` : ''}`
  
  if (href) {
    return (
      <Link href={href} className={className}>
        {children}
      </Link>
    )
  }
  
  return (
    <button 
      type={type}
      className={className} 
      onClick={onClick}
    >
      {children}
    </button>
  )
}
